import pytest
from pyminion.core import Card, Pile
from pyminion.exceptions import EmptyPile
from pyminion.expansions.base import copper, estate


def test_make_pile():
    estates: list[Card] = [estate for x in range(8)]
    estate_pile = Pile(estates)
    assert len(estate_pile) == 8
    assert estate_pile.name == "Estate"


def test_make_mixed_pile():
    mixed = Pile([estate, copper])
    assert len(mixed) == 2
    assert mixed.name == "Estate/Copper"


def test_draw_empty_pile():
    pile = Pile([copper])
    assert len(pile) == 1
    pile.remove(copper)
    assert len(pile) == 0
    with pytest.raises(EmptyPile):
        pile.remove(copper)
