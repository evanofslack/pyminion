from pyminion.models.core import Supply, Pile, Card
from pyminion.expansions.base import estate, duchy, province, copper, silver, gold
from pyminion.exceptions import PileNotFound

import pytest


def test_create_supply():

    estates = Pile([estate for x in range(8)])
    duchies = Pile([duchy for x in range(8)])
    provinces = Pile([province for x in range(8)])
    coppers = Pile([copper for x in range(8)])
    silvers = Pile([silver for x in range(8)])
    golds = Pile([gold for x in range(8)])
    supply = Supply([estates, duchies, provinces, coppers, silvers, golds])
    assert len(supply) == 6


def test_gain_card(supply: Supply):
    assert len(supply.piles[0]) == 8
    card = supply.gain_card(estate)
    assert card == estate
    assert len(supply.piles[0]) == 7


def test_gain_empty_pile_is_None(supply: Supply):
    for x in range(8):
        supply.gain_card(estate)
    assert len(supply.piles[0]) == 0
    assert supply.gain_card(estate) == None


def test_pile_not_found(supply: Supply):
    fake_card = Card(name="fake", cost=0, type="test")
    with pytest.raises(PileNotFound):
        supply.gain_card(fake_card)
