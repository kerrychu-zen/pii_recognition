from mock import Mock, patch
from pytest import fixture

from tokeniser.token import Token
import pytest

from .crf_recogniser import CrfRecogniser
from label.label_schema import SpanLabel


def get_mock_load_model():
    model = Mock()
    model.tag.return_value = ["O", "O", "PER", "O", "LOC", "O"]

    load_model = Mock()
    load_model.return_value = model
    return load_model


@fixture
def mock_tokeniser():
    tokeniser = Mock()
    tokeniser.return_value = [
        Token("This", 0, 4),
        Token("is", 5, 7),
        Token("Bob", 8, 11),
        Token("from", 12, 16),
        Token("Melbourne", 17, 26),
        Token(".", 26, 27),
    ]
    return tokeniser


@fixture
def text():
    return "This is Bob from Melbourne."


def test__get_span_labels():
    tokens = [Token("Luke", 0, 4)]
    tags = ["PER"]
    actual = CrfRecogniser._get_span_labels(tokens, tags)
    assert actual == [SpanLabel("PER", 0, 4)]

    tokens = [Token("Luke", 0, 4), Token("Skywalker", 5, 14)]
    tags = ["PER", "PER"]
    actual = CrfRecogniser._get_span_labels(tokens, tags)
    assert actual == [SpanLabel("PER", 0, 14)]

    tokens = [Token("Luke", 0, 4), Token("Skywalker", 5, 14), Token(".", 14, 15)]
    tags = ["PER", "PER", "O"]
    actual = CrfRecogniser._get_span_labels(tokens, tags)
    assert actual == [SpanLabel("PER", 0, 14), SpanLabel("O", 14, 15)]

    tokens = [Token("Luke-", 0, 5), Token("Skywalker", 5, 14)]
    tags = ["PER", "PER"]
    actual = CrfRecogniser._get_span_labels(tokens, tags)
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
    actual = CrfRecogniser._get_span_labels(tokens, tags)
    assert actual == [
        SpanLabel("O", 0, 8),
        SpanLabel("PER", 9, 23),
        SpanLabel("O", 24, 27),
        SpanLabel("PER", 28, 42),
        SpanLabel("O", 43, 60),
    ]

    tokens = []
    tags = ["O"]
    with pytest.raises(AssertionError) as err:
        CrfRecogniser._get_span_labels(tokens, tags)
    assert str(err.value) == "Length mismatch, where len(tokens)=0 and len(tags)=1"


@patch.object(target=CrfRecogniser, attribute="load_model", new=get_mock_load_model())
def test_crf_recogniser_analyse(text, mock_tokeniser):
    recogniser = CrfRecogniser(["PER", "LOC"], ["en"], "fake_path", mock_tokeniser)

    actual = recogniser.analyse(text, entities=["PER"])
    assert actual == [SpanLabel("PER", 8, 11)]

    actual = recogniser.analyse(text, entities=["PER", "LOC"])
    assert actual == [SpanLabel("PER", 8, 11), SpanLabel("LOC", 17, 26)]

    with pytest.raises(AssertionError) as err:
        recogniser.analyse(text, entities=["PER", "LOC", "TIME"])
    assert (
        str(err.value) == "Only support ['PER', 'LOC'], but got ['PER', 'LOC', 'TIME']"
    )
