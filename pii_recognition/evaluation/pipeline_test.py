from unittest.mock import patch

from .pipeline import get_recogniser, get_tokeniser
from pii_recognition.registration.registry import Registry
from typing import Any


class RegistryNoConfig:
    # class can be instantiated without passing any args
    pass


class RegistryWithConfig:
    # must pass args to instantiate the class
    def __init__(self, param_a):
        self.param_a = param_a


def mock_registry():
    # Any is equivalent to Type[Any]
    regsitry: Registry[Any] = Registry()
    regsitry.add_item(RegistryNoConfig)
    regsitry.add_item(RegistryWithConfig)
    return regsitry


@patch("pii_recognition.evaluation.pipeline.recogniser_registry", new=mock_registry())
def test_get_recogniser():
    tokeniser_setup = {"name": "RegistryNoConfig"}
    actual = get_recogniser(tokeniser_setup)["recogniser"]  # it's in meta
    assert isinstance(actual, RegistryNoConfig)

    tokeniser_setup = {"name": "RegistryWithConfig", "config": {"param_a": "value_a"}}
    actual = get_recogniser(tokeniser_setup)["recogniser"]  # it's in meta
    assert isinstance(actual, RegistryWithConfig)
    assert actual.param_a == "value_a"


@patch("pii_recognition.evaluation.pipeline.tokeniser_registry", new=mock_registry())
def test_get_tokeniser():
    tokeniser_setup = {"name": "RegistryNoConfig"}
    actual = get_tokeniser(tokeniser_setup)
    assert isinstance(actual, RegistryNoConfig)

    tokeniser_setup = {"name": "RegistryWithConfig", "config": {"param_a": "value_a"}}
    actual = get_tokeniser(tokeniser_setup)
    assert isinstance(actual, RegistryWithConfig)
    assert actual.param_a == "value_a"
