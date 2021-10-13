import pytest

from pyminion.models.cards import Deck, DiscardPile, Player, Hand, Playmat, Turn, Smithy
from pyminion.base_set.base_cards import copper, estate, smithy
from pyminion.error import InsufficientActions


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


def test_smithy_draw(turn: Turn):
    """
    Create a hand with one smithy then play that smithy.
    Assert smithy on playmat, handsize increases to 3, action count goes to 0

    """
    turn.player.hand.add(smithy)
    assert len(turn.player.hand) == 1
    turn.player.hand.cards[0].play(turn)
    assert len(turn.player.hand) == 3
    assert len(turn.player.playmat) == 1
    assert type(turn.player.playmat.cards[0]) is Smithy
    assert turn.actions == 0


def test_smithy_draw_no_actions(turn: Turn):
    turn.player.hand.add(smithy)
    turn.player.hand.cards[0].play(turn)
    turn.player.hand.add(smithy)
    with pytest.raises(InsufficientActions):
        turn.player.hand.cards[-1].play(turn)
