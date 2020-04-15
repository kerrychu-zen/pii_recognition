from unittest.mock import patch

from .registry import Registry


@patch.object(Registry, attribute="__abstractmethods__", new=set())
def test_Registry_add_item():
    class ToyClass:
        pass

    actual = Registry()  # type: ignore

    actual.add_item(ToyClass)
    assert isinstance(actual, dict)
    assert actual["ToyClass"] == ToyClass

    actual.add_item(ToyClass, "TClass")
    assert isinstance(actual, dict)
    assert actual["TClass"] == ToyClass


@patch.object(Registry, attribute="__abstractmethods__", new=set())
def test_Registry_create_instance():
    class ToyClass:
        def __init__(self, a):
            self.a = a

    registry = Registry()  # type: ignore
    registry.add_item(ToyClass)

    actual = registry.create_instance(name="ToyClass", a="a")
    assert isinstance(actual, ToyClass)
    assert actual.a == "a"
