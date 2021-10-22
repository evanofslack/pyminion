from pyminion.util import multiple_card_decision
from pyminion.exceptions import InvalidMultiCardInput
from pyminion.models.base import copper, estate
import pytest

valid_cards = [copper, copper, estate]


def test_valid_card(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Copper")
    cards = multiple_card_decision(prompt="test", valid_cards=valid_cards)
    assert type(cards) is list
    assert cards[0] == copper


def test_invalid_card(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "copper")
    with pytest.raises(InvalidMultiCardInput):
        multiple_card_decision(prompt="test", valid_cards=valid_cards)
