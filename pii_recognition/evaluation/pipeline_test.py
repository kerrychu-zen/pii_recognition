from unittest.mock import patch

from .pipeline import get_recogniser


class Simple:
    pass


class Complex:
    def __init__(self, a):
        self.a = a


def mock_registry():
    return {"Simple": Simple, "Complex": Complex}


@patch("pii_recognition.evaluation.pipeline.recogniser_registry", new=mock_registry())
def test_get_recogniser():
    actual = get_recogniser("Simple")["recogniser"]
    assert isinstance(actual, Simple)

    actual = get_recogniser("Complex", {"a": "attr_a"})["recogniser"]
    assert isinstance(actual, Complex)
    assert actual.a == "attr_a"
