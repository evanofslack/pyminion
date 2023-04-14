import pytest
from pyminion.human import multiple_card_decision
from pyminion.exceptions import InvalidMultiCardInput
from pyminion.expansions.base import copper, estate

valid_cards = [copper, copper, estate]


def test_no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert not multiple_card_decision(prompt="test", valid_cards=valid_cards)


def test_valid_card(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Copper")
    cards = multiple_card_decision(prompt="test", valid_cards=valid_cards)
    assert type(cards) is list
    assert cards[0] == copper


def test_multiple_valid_cards(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Copper, Estate")
    cards = multiple_card_decision(prompt="test", valid_cards=valid_cards)
    assert type(cards) is list
    assert len(cards) == 2
    assert cards[0] == copper
    assert cards[1] == estate


def test_invalid_card(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Silver")
    with pytest.raises(
        InvalidMultiCardInput, match="Invalid input, Silver is not a valid card"
    ):
        multiple_card_decision(prompt="test", valid_cards=valid_cards)


def test_too_many_valid_cards(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Copper, Copper, Copper")
    with pytest.raises(
        InvalidMultiCardInput,
        match="Invalid input, attempted to select too many copies of Copper",
    ):
        multiple_card_decision(prompt="test", valid_cards=valid_cards)


def test_confirm_case_insensitive(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Copper, copper, estate")
    cards = multiple_card_decision(prompt="test", valid_cards=valid_cards)
    assert len(cards) == 3
    assert cards[0] == copper
    assert cards[1] == copper
    assert cards[2] == estate


def test_invalid_spelling(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "copper, coopper, copper")
    with pytest.raises(
        InvalidMultiCardInput, match="Invalid input, coopper is not a valid card"
    ):
        multiple_card_decision(prompt="test", valid_cards=valid_cards)
