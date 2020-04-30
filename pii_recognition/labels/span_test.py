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
    span_labels = [
        SpanLabel("Bob", "PER", 8, 11),
        SpanLabel("Melbourne", "LOC", 17, 26),
    ]
    tokens = [
        Token("This", 0, 4),
        Token("is", 5, 7),
        Token("Bob", 8, 11),
        Token("from", 12, 16),
        Token("Melbourne", 17, 26),
        Token(".", 26, 27),
    ]
    actual = span_labels_to_token_labels(span_labels, tokens)
    assert [x.entity_type for x in actual] == ["O", "O", "PER", "O", "LOC", "O"]

    # TODO: add test case where span across multiple tokens


def test_token_labels_to_span_labels():
    token_labels = [TokenLabel("Luke", 0, 4, "PER")]
    actual = token_labels_to_span_labels(token_labels)
    assert actual == [SpanLabel("Luke", "PER", 0, 4)]

    tokens = [Token("Luke", 0, 4), Token("Skywalker", 5, 14)]
    tags = ["PER", "PER"]
    actual = token_labels_to_span_labels(tokens, tags)
    assert actual == [SpanLabel("PER", 0, 14)]

    tokens = [Token("Luke", 0, 4), Token("Skywalker", 5, 14), Token(".", 14, 15)]
    tags = ["PER", "PER", "O"]
    actual = token_labels_to_span_labels(tokens, tags)
    assert actual == [SpanLabel("PER", 0, 14), SpanLabel("O", 14, 15)]

    tokens = [Token("Luke-", 0, 5), Token("Skywalker", 5, 14)]
    tags = ["PER", "PER"]
    actual = token_labels_to_span_labels(tokens, tags)
    assert actual == [SpanLabel("PER", 0, 14)]

    tokens = [
        Token("one", 0, 3),
        Token("day", 4, 7),
        Token(",", 7, 8),
        Token("Luke", 9, 13),
        Token("Skywalker", 14, 23),
        Token("and", 24, 27),
        Token("Wedge", 28, 33),
        Token("Antilles", 34, 42),
        Token("recover", 43, 50),
        Token("a", 51, 52),
        Token("message", 53, 60),
    ]
    tags = ["O", "O", "O", "PER", "PER", "O", "PER", "PER", "O", "O", "O"]
    actual = token_labels_to_span_labels(tokens, tags)
    assert actual == [
        SpanLabel("O", 0, 8),
        SpanLabel("PER", 9, 23),
        SpanLabel("O", 24, 27),
        SpanLabel("PER", 28, 42),
        SpanLabel("O", 43, 60),
    ]

    tokens = [Token(".", 0, 1)]
    tags = ["O", "O"]
    with pytest.raises(AssertionError) as err:
        token_labels_to_span_labels(tokens, tags)
    assert str(err.value) == "Length mismatch, where len(tokens)=1 and len(tags)=2"
