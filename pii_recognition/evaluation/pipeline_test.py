from unittest.mock import patch

from pytest import raises

from .pipeline import get_recogniser


@patch(
    "pii_recognition.registry",
    new={"fake_model": "fake_value"},
)
def test_get_recogniser():
    actual = get_recogniser("fake_model")
    assert actual == "fake_value"

    with raises(KeyError) as err:
        get_recogniser("non_exist_model")
    assert str(err.value) == "'non_exist_model'"
