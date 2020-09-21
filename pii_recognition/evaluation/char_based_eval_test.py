import pytest

from pii_recognition.evaluation.char_based_eval import encode_labels
from pii_recognition.labels.schema import SpanLabel


def test_encode_labels():
    with pytest.raises(ValueError) as err:
        encode_labels(text_length=10,
                      span_labels=[],
                      label_to_int={
                          "LOC": 1,
                          "default": 5
                      })
    assert str(err.value) == "Value of default must be 0!"

    spans = [SpanLabel(entity_type="LOC", start=5, end=8)]
    with pytest.raises(ValueError) as err:
        encode_labels(text_length=7,
                      span_labels=spans,
                      label_to_int={"LOC": 1})
    assert str(err.value) == "Span index is out of text range."

    spans = [SpanLabel(entity_type="LOC", start=5, end=8)]
    actual = encode_labels(text_length=10,
                           span_labels=spans,
                           label_to_int={"LOC": 1})
    assert actual == [0, 0, 0, 0, 0, 1, 1, 1, 0, 0]

    spans = [
        SpanLabel(entity_type="LOC", start=5, end=8),
        SpanLabel(entity_type="PER", start=10, end=15),
        SpanLabel(entity_type="PERSON", start=2, end=5)
    ]
    actual = encode_labels(text_length=20,
                           span_labels=spans,
                           label_to_int={
                               "LOC": 1,
                               "PER": 2,
                               "PERSON": 2
                           })
    assert actual == [
        0, 0, 2, 2, 2, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0
    ]
