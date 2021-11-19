import pytest
from pyminion.exceptions import EmptyPile
from pyminion.expansions.base import copper, estate
from pyminion.models.core import Pile


def make_empty_pile():
    empty = Pile()
    assert len(empty) == 0
    assert empty.name is None


def test_make_pile():
    estates = [estate for x in range(8)]
    estate_pile = Pile(estates)
    assert len(estate_pile) == 8
    assert estate_pile.name == "Estate"


def test_make_mixed_pile():
    mixed = Pile([estate, copper])
    assert len(mixed) == 2
    assert mixed.name == "Mixed"


def test_draw_empty_pile():
    pile = Pile([copper])
    assert len(pile) == 1
    pile.remove(copper)
    assert len(pile) == 0
    with pytest.raises(EmptyPile):
        pile.remove(copper)
