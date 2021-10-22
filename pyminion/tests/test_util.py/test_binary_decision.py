from pyminion.util import binary_decision


def test_yes_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert binary_decision(prompt="test") is True


def test_no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert binary_decision(prompt="test") is False


def test_invalid_input(monkeypatch):
    from pyminion.exceptions import InvalidBinaryInput
    import pytest

    monkeypatch.setattr("builtins.input", lambda _: "")
    with pytest.raises(InvalidBinaryInput):
        binary_decision(prompt="test")
