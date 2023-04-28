import pytest
from pyminion.human import deck_position_decision
from pyminion.exceptions import InvalidDeckPositionInput


def test_no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    with pytest.raises(
        InvalidDeckPositionInput, match="Invalid input, '' is not a valid position"
    ):
        deck_position_decision("test", 10)


def test_invalid_string_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "abc")
    with pytest.raises(
        InvalidDeckPositionInput, match="Invalid input, 'abc' is not a valid position"
    ):
        deck_position_decision("test", 10)


def test_top(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "top")
    assert deck_position_decision("test", 10) == 10


def test_bottom(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Bottom")
    assert deck_position_decision("test", 10) == 0


def test_valid_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "4")
    assert deck_position_decision("test", 10) == 3


def test_too_small_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "-1")
    with pytest.raises(
        InvalidDeckPositionInput, match="Invalid input, '-1' is less than the minimum value of 1"
    ):
        deck_position_decision("test", 10)


def test_too_large_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "12")
    with pytest.raises(
        InvalidDeckPositionInput, match="Invalid input, '12' is greater than the maximum value of 11"
    ):
        deck_position_decision("test", 10)
