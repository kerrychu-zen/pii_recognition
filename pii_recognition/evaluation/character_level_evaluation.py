from dataclasses import asdict
from typing import Any, Dict, List

from pii_recognition.evaluation.metrics import (
    compute_label_precision,
    compute_label_recall,
)
from pii_recognition.labels.schema import Entity


def encode_labels(
    text_length: int, entities: List[Entity], label_to_int: Dict[Any, int],
) -> List[int]:
    """Encode span-based labels into integers.

    Encode a text at character level according to text-span labels as well as a mapping
    defined by `label_to_int`. Note multi-tagging is not supported. One entity can have
    only one label tag.

    Args:
        text_length: length of a text.
        entities: entities being identified in a text.
        label_to_int: a mapping between entity labels and integers.

    Returns:
        Integer code of the text.
    """
    if 0 in label_to_int.values():
        raise ValueError(
            "Value 0 is reserved! If a character does not belong to any classes, it "
            "will be assigned with 0."
        )
    code = [0] * text_length

    for span in entities:
        s = span.start
        e = span.end
        if e > text_length:
            raise ValueError(
                f"Span index is out of range: text length is "
                f"{text_length} but got span index {e}."
            )
        label_name = span.entity_type
        try:
            label_code = label_to_int[label_name]
        except KeyError as err:
            raise Exception(
                f"Label {str(err)} is not presented in 'label_to_int' mapping."
            )

        code[s:e] = [label_code] * (e - s)

    return code


def compute_entity_precisions_for_prediction(
    text_length: int,
    true_entities: List[Entity],
    pred_entities: List[Entity],
    label_mapping: Dict,
) -> List[Dict]:
    true_code: List[int] = encode_labels(text_length, true_entities, label_mapping)

    precisions: List = []
    for pred_entity in pred_entities:
        pred_entity_code: List[int] = encode_labels(
            text_length, [pred_entity], label_mapping
        )
        int_label: int = label_mapping[pred_entity.entity_type]
        score = compute_label_precision(true_code, pred_entity_code, int_label)

        span_dict = asdict(pred_entity)
        span_dict.update({"precision": score})
        precisions.append(span_dict)

    return precisions


def compute_entity_recalls_for_ground_truth(
    text_length: int,
    true_entities: List[Entity],
    pred_entities: List[Entity],
    label_mapping: Dict,
) -> List[Dict]:
    pred_code: List[int] = encode_labels(text_length, pred_entities, label_mapping)

    recalls: List = []
    for true_entity in true_entities:
        true_entity_code: List[int] = encode_labels(
            text_length, [true_entity], label_mapping
        )
        int_label: int = label_mapping[true_entity.entity_type]
        score = compute_label_recall(true_entity_code, pred_code, int_label)

        span_dict = asdict(true_entity)
        span_dict.update({"recall": score})
        recalls.append(span_dict)

    return recalls
