import logging
from dataclasses import asdict
from typing import Dict, List

from pii_recognition.evaluation.metrics import (
    compute_label_precision,
    compute_label_recall,
)
from pii_recognition.labels.schema import SpanLabel


def encode_labels(
    text_length: int, span_labels: List[SpanLabel], label_mapping: Dict
) -> List[int]:
    if "default" in label_mapping:
        coding = [label_mapping["default"]] * text_length
    else:
        logging.info("Default value 0 is assinged for label encoding.")
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
        label_code = label_mapping[label_name]

        coding[s:e] = [label_code] * (e - s)

    return coding


def _precisions_recalls_support(
    text_length: int,
    true_spans: List[SpanLabel],
    pred_spans: List[SpanLabel],
    label_mapping: Dict,
    compute_for: str,
) -> Dict:
    if compute_for not in {"precision", "recall"}:
        raise ValueError(
            "Available options for computation are: 'precision', 'recall'."
        )

    config = {
        "precision": {"targeted": pred_spans, "untargeted": true_spans},
        "recall": {"targeted": true_spans, "untargeted": pred_spans},
    }

    coding = encode_labels(
        text_length, config[compute_for]["untargeted"], label_mapping
    )

    scores = []
    for span in config[compute_for]["targeted"]:
        span_coding = encode_labels(text_length, [span], label_mapping)
        if compute_for == "precision":
            score = compute_label_precision(coding, span_coding, span.entity_type)
        elif compute_for == "recall":
            score = compute_label_recall(span_coding, coding, span.entity_type)
        score.append(asdict(span).update({compute_for: scores}))

    return scores


def compute_precisions_for_predicted_entities(
    text_length: int,
    true_spans: List[SpanLabel],
    pred_spans: List[SpanLabel],
    label_mapping: Dict,
) -> Dict:
    _precisions_recalls_support(
        text_length, true_spans, pred_spans, label_mapping, compute_for="precision"
    )


def compute_recalls_for_ground_truth_entities(
    text_length: int,
    true_spans: List[SpanLabel],
    pred_spans: List[SpanLabel],
    label_mapping: Dict,
) -> Dict:
    _precisions_recalls_support(
        text_length, true_spans, pred_spans, label_mapping, compute_for="recall"
    )
