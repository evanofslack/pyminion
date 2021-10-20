import pytest

from pyminion.expansions.base import copper, silver, gold, estate, duchy, province
from pyminion.models.core import (
    Pile,
    Deck,
    DiscardPile,
    Hand,
    Playmat,
    Player,
    Turn,
    Supply,
    Trash,
)


NUM_COPPER = 7
NUM_ESTATE = 3


@pytest.fixture
def deck():
    start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]
    deck = Deck(cards=start_cards)
    return deck


@pytest.fixture
def player(deck):
    discard = DiscardPile()
    hand = Hand()
    playmat = Playmat()
    player_id = "Test"
    player = Player(
        deck=deck, discard=discard, hand=hand, playmat=playmat, player_id=player_id
    )
    return player


@pytest.fixture
def turn(player):
    turn = Turn(player=player)
    return turn


@pytest.fixture
def trash():
    trash = Trash()
    return trash


@pytest.fixture
def supply():
    estates = Pile([estate for x in range(8)])
    duchies = Pile([duchy for x in range(8)])
    provinces = Pile([province for x in range(8)])
    coppers = Pile([copper for x in range(60)])
    silvers = Pile([silver for x in range(40)])
    golds = Pile([gold for x in range(30)])
    supply = Supply([estates, duchies, provinces, coppers, silvers, golds])
    return supply
