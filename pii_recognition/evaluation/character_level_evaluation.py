import logging
from dataclasses import asdict
from typing import Dict, List, Any

from pii_recognition.evaluation.metrics import (
    compute_label_precision,
    compute_label_recall,
)
from pii_recognition.labels.schema import SpanLabel


def encode_labels(
    text_length: int, span_labels: List[SpanLabel], label_to_int: Dict[Any, int]
) -> List[int]:
    """Encode span-based labels into integers.

    Encode a text at character level according to text-span labels as well as a mapping
    defined by `label_to_int`. Regarding to the mapping, it must have a key of "default"
    to map every non-labeled charater to this default value.

    Args:
        text_length: length of a text.
        spans_labels: entities being identified in a text represented by text-spans.
        label_to_int: a mapping between entity labels and integers.

    Returns:
        Integer coding of the text.
    """
    if "default" in label_to_int:
        coding = [label_to_int["default"]] * text_length
    else:
        logging.info("Default is not given, value 0 is assinged for default.")
        assigned_default = 0
        coding = [assigned_default] * text_length

    for span in span_labels:
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

        coding[s:e] = [label_code] * (e - s)

    return coding


def _precisions_recalls_support(
    text_length: int,
    true_spans: List[SpanLabel],
    pred_spans: List[SpanLabel],
    label_mapping: Dict,
    compute_for: str,
) -> List[Dict]:
    if compute_for not in {"precision", "recall"}:
        raise ValueError(
            f"Available options for computation are: "
            f"'precision', 'recall' but got {compute_for}"
        )

    config = {
        "precision": {"loop": pred_spans, "no_loop": true_spans},
        "recall": {"loop": true_spans, "no_loop": pred_spans},
    }

    coding: List[int] = encode_labels(
        text_length, config[compute_for]["no_loop"], label_mapping
    )

    scores: List = []
    for span in config[compute_for]["loop"]:
        span_coding: List[int] = encode_labels(text_length, [span], label_mapping)
        int_label: int = label_mapping[span.entity_type]

        if compute_for == "precision":
            score = compute_label_precision(coding, span_coding, int_label)
        elif compute_for == "recall":
            score = compute_label_recall(span_coding, coding, int_label)

        span_dict = asdict(span)
        span_dict.update({compute_for: score})
        scores.append(span_dict)

    return scores


def compute_entity_precisions_for_prediction(
    text_length: int,
    true_spans: List[SpanLabel],
    pred_spans: List[SpanLabel],
    label_mapping: Dict,
) -> List[Dict]:
    return _precisions_recalls_support(
        text_length, true_spans, pred_spans, label_mapping, compute_for="precision"
    )


def compute_entity_recalls_for_ground_truth(
    text_length: int,
    true_spans: List[SpanLabel],
    pred_spans: List[SpanLabel],
    label_mapping: Dict,
) -> List[Dict]:
    return _precisions_recalls_support(
        text_length, true_spans, pred_spans, label_mapping, compute_for="recall"
    )
