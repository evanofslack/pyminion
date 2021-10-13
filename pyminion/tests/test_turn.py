import pytest

from pyminion.models.cards import Deck, DiscardPile, Player, Hand, Playmat, Turn
from pyminion.base_set.base_cards import copper, silver, gold, estate, duchy, province

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
    player = Player(deck=deck, discard=discard, hand=hand, playmat=playmat)
    return player


@pytest.fixture
def turn(player):
    turn = Turn(player=player)
    return turn


def test_create_turn(player: Player):
    turn = Turn(player=player)
    assert turn.actions == 1
    assert turn.money == 0
    assert turn.buys == 1


def test_play_copper(turn: Turn):
    """
    Create a hand with one copper then play that copper.
    Assert copper moves from hand to playmat and money increases to 1

    """
    turn.player.hand.add(copper)
    assert len(turn.player.hand) == 1
    turn.player.hand.cards[0].play(turn)
    assert turn.money == 1
    assert len(turn.player.hand) == 0
    assert len(turn.player.playmat) == 1
