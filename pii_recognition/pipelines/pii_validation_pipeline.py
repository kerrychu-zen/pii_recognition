from typing import Dict, List, Optional, Set, Tuple, Union, FrozenSet

from pakkr import returns
from pii_recognition.data_readers.data import Data
from pii_recognition.data_readers.presidio_fake_pii_reader import PresidioFakePiiReader
from pii_recognition.evaluation.character_level_evaluation import (
    EntityPrecision,
    EntityRecall,
    TextScore,
    build_label_mapping,
    compute_entity_precisions_for_prediction,
    compute_entity_recalls_for_ground_truth,
    compute_pii_detection_f1,
)
from pii_recognition.recognisers import registry as recogniser_registry
from pii_recognition.recognisers.entity_recogniser import EntityRecogniser
from pii_recognition.utils import dump_to_json_file


@returns(Data)
def read_benchmark_data(benchmark_data_file: str) -> Data:
    reader = PresidioFakePiiReader()
    return reader.build_data(benchmark_data_file)


@returns(Data)
def identify_pii_entities(
    data: Data, recogniser_name: str, recogniser_params: Dict
) -> Data:
    recogniser: EntityRecogniser = recogniser_registry.create_instance(
        recogniser_name, recogniser_params
    )

    for item in data.items:
        item.pred_labels = recogniser.analyse(item.text, recogniser.supported_entities)
    return data


@returns(List)
def calculate_precisions_and_recalls(
    data: Data,
    grouped_targeted_labels: List[Set[str]],
    nontargeted_labels: Optional[Set[str]] = None,
) -> List[TextScore]:
    label_mapping = build_label_mapping(grouped_targeted_labels, nontargeted_labels)

    scores = []
    for item in data.items:
        if item.pred_labels:
            pred_labels = item.pred_labels
        else:  # pred_labels could be None
            pred_labels = []

        ent_precisions = compute_entity_precisions_for_prediction(
            len(item.text), item.true_labels, pred_labels, label_mapping
        )
        ent_recalls = compute_entity_recalls_for_ground_truth(
            len(item.text), item.true_labels, pred_labels, label_mapping
        )
        ticket_score = TextScore(precisions=ent_precisions, recalls=ent_recalls)
        scores.append(ticket_score)

    return scores


@returns(Dict)
def calculate_aggregate_metrics(
    scores: List[TextScore], f1_beta: float = 1.0
) -> Dict[str, float]:
    results = dict()
    exact_match = get_rollup_f1s_on_pii(scores, f1_beta, recall_threshold=None)
    results["exact_match_f1"] = sum(exact_match) / len(exact_match)

    partial_match = get_rollup_f1s_on_pii(scores, f1_beta, recall_threshold=0.5)
    results["partial_match_f1_threshold_at_50%"] = sum(partial_match) / len(
        partial_match
    )
    return results


@returns
def report_results(results: Dict[str, float], dump_file: str):
    dump_to_json_file(results, dump_file)


def get_rollup_f1s_on_pii(
    scores: List[TextScore], f1_beta: float, recall_threshold: Optional[float]
) -> List[float]:
    f1s = []
    for text_score in scores:
        precisions = [p.precision for p in text_score.precisions]
        recalls = [r.recall for r in text_score.recalls]
        f1 = compute_pii_detection_f1(precisions, recalls, recall_threshold, f1_beta)
        f1s.append(f1)
    return f1s


def _update_score_table(
    score_table: Dict[FrozenSet, Dict], new_item: Union[EntityPrecision, EntityRecall]
):
    entity_label = new_item.entity.entity_type
    for label_set in score_table.keys():
        if entity_label in label_set:
            if isinstance(new_item, EntityPrecision):
                score_table[label_set]["precisions"].append(new_item.precision)
            elif isinstance(new_item, EntityRecall):
                score_table[label_set]["recalls"].append(new_item.recall)
    return score_table


def get_rollup_f1s_on_types(
    scores: List[TextScore], grouped_targeted_labels: List[Set[str]], f_beta: float,
) -> Dict[FrozenSet, float]:
    """Calculate f scores for grouped types of entities.

    There are entity labels/types being grouped and passed to this function, with which
    we can calculate f scores. As a result, every group in the label groups will get
    one f score to represent how a system did on predicting the entity(ies).

    Args:
        scores: a list of text scores providing info including precisions and recalls.
        grouped_targeted_labels: entity labels we are interested that have been
            separated by groups, for example, [{"PER", "PERSON"}, {"ORG"}].
        f_beta: beta value for f score.

    Returns:
        A dictionary that key is an entity group and value is f score for that group.
    """
    score_table: Dict[FrozenSet, Dict] = {
        frozenset(label_set): {"precisions": [], "recalls": [], "f1": None}
        for label_set in grouped_targeted_labels
    }

    # update score table
    for text_score in scores:
        for precision in text_score.precisions:
            score_table = _update_score_table(score_table, precision)
        for recall in text_score.recalls:
            score_table = _update_score_table(score_table, recall)

    # average precisions and recalls
    for key, value in score_table.items():
        value["f1"] = compute_pii_detection_f1(value["precisions"], value["recalls"])
    return {key: value["f1"] for key, value in score_table.items()}
