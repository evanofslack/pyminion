import pytest

from pyminion.base_set.base_cards import copper, estate
from pyminion.models.base import Deck, DiscardPile, Hand, Playmat, Player, Turn


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
    player = Player(deck=deck, discard=discard, hand=hand, playmat=playmat)
    return player


@pytest.fixture
def turn(player):
    turn = Turn(player=player)
    return turn
