import pytest

from pii_recognition.tokenisation.token_schema import Token

from .schema import SpanLabel, TokenLabel
from .span import is_substring, span_labels_to_token_labels, token_labels_to_span_labels


def test_is_substring():
    assert is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(4, 8))
    assert is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(5, 8))
    assert is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(4, 9))

    assert not is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(6, 8))
    assert not is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(6, 9))
    assert not is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(5, 7))
    assert not is_substring(segment_A_start_end=(5, 8), segment_B_start_end=(4, 7))


def test_span_labels_to_token_labels():
    # reference sentence: "This is Bob from Melbourne."
    span_labels = [
        SpanLabel("PER", 8, 11),
        SpanLabel("LOC", 17, 26),
    ]
    tokens = [
        Token(0, 4),
        Token(5, 7),
        Token(8, 11),
        Token(12, 16),
        Token(17, 26),
        Token(26, 27),
    ]
    actual = span_labels_to_token_labels(span_labels, tokens)
    assert [x.entity_type for x in actual] == ["O", "O", "PER", "O", "LOC", "O"]

    # TODO: add test case where span across multiple tokens


def test_token_labels_to_span_labels():
    #
    token_labels = [TokenLabel(0, 4, "PER")]
    actual = token_labels_to_span_labels(token_labels)
    assert actual == [SpanLabel("PER", 0, 4)]

    # text: Luke
    token_labels = [
        TokenLabel(0, 4, "PER"),
        TokenLabel(5, 14, "PER"),
    ]
    actual = token_labels_to_span_labels(token_labels)
    assert actual == [SpanLabel("PER", 0, 14)]

    # text: Luke Skywalker
    token_labels = [
        TokenLabel(0, 4, "PER"),
        TokenLabel(5, 14, "PER"),
        TokenLabel(14, 15, "O"),
    ]
    actual = token_labels_to_span_labels(token_labels)
    assert actual == [SpanLabel("PER", 0, 14), SpanLabel("O", 14, 15)]

    # text: Luke-Skywalker
    token_labels = [TokenLabel(0, 5, "PER"), TokenLabel(5, 14, "PER")]
    actual = token_labels_to_span_labels(token_labels)
    assert actual == [SpanLabel("PER", 0, 14)]

    # text: one day, Luke Skywalker and Wedge Antilles recover a message
    token_labels = [
        TokenLabel(0, 3, "O"),
        TokenLabel(4, 7, "O"),
        TokenLabel(7, 8, "O"),
        TokenLabel(9, 13, "PER"),
        TokenLabel(14, 23, "PER"),
        TokenLabel(24, 27, "O"),
        TokenLabel(28, 33, "PER"),
        TokenLabel(34, 42, "PER"),
        TokenLabel(43, 50, "O"),
        TokenLabel(51, 52, "O"),
        TokenLabel(53, 60, "O"),
    ]
    actual = token_labels_to_span_labels(token_labels)
    assert actual == [
        SpanLabel("O", 0, 8),
        SpanLabel("PER", 9, 23),
        SpanLabel("O", 24, 27),
        SpanLabel("PER", 28, 42),
        SpanLabel("O", 43, 60),
    ]
