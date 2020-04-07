from .recogniser_registry import RecogniserRegistry


def test_RecogniserRegistry():
    actual = RecogniserRegistry()
    assert isinstance(actual, dict)
    assert len(actual.keys()) > 0
    assert len(actual.keys()) == len(actual.values())
