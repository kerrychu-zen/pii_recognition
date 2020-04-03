from .path import Path
from pytest import raises
from unittest.mock import patch, Mock


@patch.object(Path, attribute="__abstractmethods__", new=set())
def test_Path_attributes():
    with patch.object(Path, attribute="get_pattern") as mock_get_pattern:
        mock_get_pattern.return_value = None
        actual = Path("fake_path")
    assert actual.path == "fake_path"
    assert actual.valid == False

    with patch.object(Path, attribute="get_pattern") as mock_get_pattern:
        mock_get_pattern.return_value.groupdict.return_value = {"version": 0.0}
        actual = Path("fake_path")
    assert actual.version == 0.0
    assert actual.path == "fake_path"
    assert actual.valid == True

