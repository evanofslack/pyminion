from pyminion.models.base import Supply, Pile
from pyminion.base_set.base_cards import estate, duchy, province, copper, silver, gold


def test_create_supply():

    estates = Pile([estate for x in range(8)])
    duchies = Pile([duchy for x in range(8)])
    provinces = Pile([province for x in range(8)])
    coppers = Pile([copper for x in range(8)])
    silvers = Pile([silver for x in range(8)])
    golds = Pile([gold for x in range(8)])

    supply = Supply([estates, duchies, provinces, coppers, silvers, golds])

    assert len(supply) == 6


def test_gain_from_pile(supply: Supply):
    assert len(supply.piles[3]) == 8

    for pile in supply.piles:
        if pile.name == "Copper":
            card = pile.remove(copper)

    assert len(supply.piles[3]) == 7
    assert card == copper
