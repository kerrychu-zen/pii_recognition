from .detokeniser_registry import DetokeniserRegistry


def test_DetokeniserRegistry():
    actual = DetokeniserRegistry()
    assert isinstance(actual, dict)
    assert len(actual.keys()) > 0
