import pytest
from pii_recognition.labels.schema import SpanLabel

from pii_recognition.evaluation.character_level_evaluation import (
    encode_labels,
    compute_entity_precisions_for_prediction,
    compute_entity_recalls_for_ground_truth,
)


def test_encode_labels_with_custom_default():
    coding = encode_labels(3, [], {"default": 5})
    assert coding == [5, 5, 5]


def test_encode_labels_for_multi_labels():
    spans = [
        SpanLabel(entity_type="LOC", start=5, end=8),
        SpanLabel(entity_type="PER", start=10, end=15),
        SpanLabel(entity_type="PERSON", start=2, end=5),
    ]

    # entity PER and PERSON map to the same int
    actual = encode_labels(20, spans, {"LOC": 1, "PER": 2, "PERSON": 2})
    assert actual == [0, 0, 2, 2, 2, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0]


def test_encode_labels_for_missing_label_in_mapping():
    spans = [
        SpanLabel(entity_type="LOC", start=5, end=8),
        SpanLabel(entity_type="PER", start=10, end=15),
    ]

    with pytest.raises(Exception) as error:
        encode_labels(20, spans, {"LOC": 1})
    assert str(error.value) == (
        "Label 'PER' is not presented in 'label_to_int' mapping."
    )


def test_encode_labels_for_span_beyond_range():
    spans = [SpanLabel(entity_type="LOC", start=3, end=7)]

    with pytest.raises(ValueError) as error:
        encode_labels(5, spans, {"LOC": 1})
    assert str(error.value) == (
        "Span index is out of range: text length is 5 but got span index 7."
    )


def test_compute_precisions_recalls_for_exact_match():
    true_spans = pred_spans = [SpanLabel(entity_type="LOC", start=3, end=7)]
    label_to_int = {"LOC": 1}

    precisions = compute_entity_precisions_for_prediction(
        10, true_spans, pred_spans, label_to_int
    )
    recalls = compute_entity_recalls_for_ground_truth(
        10, true_spans, pred_spans, label_to_int
    )

    assert precisions == [
        {"entity_type": "LOC", "start": 3, "end": 7, "precision": 1.0}
    ]
    assert recalls == [{"entity_type": "LOC", "start": 3, "end": 7, "recall": 1.0}]


def test_compute_precisions_recalls_for_pred_subset_of_true():
    true_spans = [SpanLabel(entity_type="LOC", start=3, end=7)]
    pred_spans = [SpanLabel(entity_type="LOC", start=4, end=6)]
    label_to_int = {"LOC": 1}

    precisions = compute_entity_precisions_for_prediction(
        10, true_spans, pred_spans, label_to_int
    )
    recalls = compute_entity_recalls_for_ground_truth(
        10, true_spans, pred_spans, label_to_int
    )

    assert precisions == [
        {"entity_type": "LOC", "start": 4, "end": 6, "precision": 1.0}
    ]
    assert recalls == [{"entity_type": "LOC", "start": 3, "end": 7, "recall": 0.5}]


def test_compute_precisions_recalls_for_pred_superset_of_true():
    true_spans = [SpanLabel(entity_type="LOC", start=3, end=6)]
    pred_spans = [SpanLabel(entity_type="LOC", start=2, end=8)]
    label_to_int = {"LOC": 1}

    precisions = compute_entity_precisions_for_prediction(
        10, true_spans, pred_spans, label_to_int
    )
    recalls = compute_entity_recalls_for_ground_truth(
        10, true_spans, pred_spans, label_to_int
    )

    assert precisions == [
        {"entity_type": "LOC", "start": 2, "end": 8, "precision": 0.5}
    ]
    assert recalls == [{"entity_type": "LOC", "start": 3, "end": 6, "recall": 1.0}]


def test_compute_precisions_recalls_for_pred_overlap_true():
    true_spans = [SpanLabel(entity_type="LOC", start=2, end=7)]
    pred_spans = [SpanLabel(entity_type="LOC", start=5, end=9)]
    label_to_int = {"LOC": 1}

    precisions = compute_entity_precisions_for_prediction(
        10, true_spans, pred_spans, label_to_int
    )
    recalls = compute_entity_recalls_for_ground_truth(
        10, true_spans, pred_spans, label_to_int
    )

    assert precisions == [
        {"entity_type": "LOC", "start": 5, "end": 9, "precision": 0.5}
    ]
    assert recalls == [{"entity_type": "LOC", "start": 2, "end": 7, "recall": 0.4}]
