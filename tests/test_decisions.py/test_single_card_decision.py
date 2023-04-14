import pytest
from pyminion.human import single_card_decision
from pyminion.exceptions import InvalidSingleCardInput
from pyminion.expansions.base import copper, estate

valid_cards = [copper, copper, estate]


def test_no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert not single_card_decision(prompt="test", valid_cards=valid_cards)


def test_valid_card(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Copper")
    card = single_card_decision(prompt="test", valid_cards=valid_cards)
    assert card == copper


def test_invalid_card(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Silver")
    with pytest.raises(
        InvalidSingleCardInput, match="Invalid input, Silver is not a valid selection"
    ):
        single_card_decision(prompt="test", valid_cards=valid_cards)


def test_invalid_spelling(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "coopper")
    with pytest.raises(
        InvalidSingleCardInput, match="Invalid input, coopper is not a valid selection"
    ):
        single_card_decision(prompt="test", valid_cards=valid_cards)


def test_confirm_case_insensitive(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "copper")
    card = single_card_decision(prompt="test", valid_cards=valid_cards)
    assert card == copper
