from pyminion.decisions import single_card_decision
from pyminion.exceptions import InvalidSingleCardInput
from pyminion.models.base import copper, estate
import pytest

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
    with pytest.raises(InvalidSingleCardInput):
        single_card_decision(prompt="test", valid_cards=valid_cards)


def test_confirm_case_insensetive(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "copper")
    card = single_card_decision(prompt="test", valid_cards=valid_cards)
    assert card == copper
