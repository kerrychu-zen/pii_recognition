from .tokeniser_registry import TokeniserRegistry


def test_TokeniserRegistry():
    actual = TokeniserRegistry()
    assert isinstance(actual, dict)
    assert len(actual.keys()) > 0
