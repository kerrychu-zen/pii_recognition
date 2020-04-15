from unittest.mock import patch

from pytest import raises

from .registry import Registry


@patch.object(Registry, attribute="__abstractmethods__", new=set())
def test_Registry():
    def toy_func():
        pass

    class ToyClass:
        pass

    toy_assignment = ""

    actual = Registry()  # type: ignore

    actual.add_item(ToyClass)
    assert isinstance(actual, dict)
    assert actual["ToyClass"] == ToyClass

    with raises(TypeError) as err:
        actual.add_item(toy_func)
    assert str(err.value) == "The registered item must be a class object."


    with raises(TypeError) as err:
        actual.add_item(toy_assignment)
    assert str(err.value) == "The registered item must be a class object."
