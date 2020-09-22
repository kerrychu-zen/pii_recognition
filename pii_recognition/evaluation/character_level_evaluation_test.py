import pytest
from pii_recognition.labels.schema import SpanLabel

from pii_recognition.evaluation.character_level_evaluation import encode_labels


def test_encode_labels_with_default_int():
    coding = encode_labels(3, span_labels=[], label_to_int={})
    assert coding == [0, 0, 0]


def test_encode_labels_with_custom_int():
    # customise default to 5
    coding = encode_labels(3, span_labels=[], label_to_int={"default": 5})
    assert coding == [5, 5, 5]


def test_encode_labels_for_span_out_of_range():
    # text length is 5 but got an entity from 3 to 7
    spans = [SpanLabel(entity_type="LOC", start=3, end=7)]
    with pytest.raises(ValueError) as error:
        encode_labels(5, spans, {"LOC": 1})
    assert str(error.value) == (
        "Span index is out of range: text length is 5 but got span index 7."
    )


def test_encode_labels_for_multi_labels():
    spans = [
        SpanLabel(entity_type="LOC", start=5, end=8),
        SpanLabel(entity_type="PER", start=10, end=15),
        SpanLabel(entity_type="PERSON", start=2, end=5),
    ]
    # entity PER and PERSON map to the same int
    actual = encode_labels(20, spans, {"LOC": 1, "PER": 2, "PERSON": 2})
    assert actual == [0, 0, 2, 2, 2, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0]


def test_encode_labels_for_uncovered_label():
    spans = [
        SpanLabel(entity_type="LOC", start=5, end=8),
        SpanLabel(entity_type="PER", start=10, end=15),
    ]
    # entity PER is not covered
    with pytest.raises(KeyError) as error:
        encode_labels(20, spans, {"LOC": 1})
    assert str(error.value) == "'PER'"
