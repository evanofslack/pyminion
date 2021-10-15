from pyminion.models.base import Player, Turn
from pyminion.base_set.base_cards import copper, estate
from pyminion.exceptions import InsufficientMoney, InsufficientBuys

import pytest


def test_create_turn(player: Player):
    turn = Turn(player=player)
    assert turn.actions == 1
    assert turn.money == 0
    assert turn.buys == 1


def test_draw_five(turn: Turn):
    assert len(turn.player.hand) == 0
    turn.draw_five()
    assert len(turn.player.hand) == 5


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


def test_play_multiple_copper(turn: Turn):
    """
    Create a hand with 6 estates and 3 coppers. Play all coppers.
    Assert 3 coppers end up on playmat, 6 estates remain in hand,
    and that money increases to 3

    """
    for i in range(3):
        turn.player.hand.add(estate)
        turn.player.hand.add(estate)
        turn.player.hand.add(copper)
    assert len(turn.player.hand) == 9

    i = 0  # Pythonic way to pop in loop?
    while i < len(turn.player.hand):
        if turn.player.hand.cards[i] == copper:
            turn.player.hand.cards[i].play(turn)
        else:
            i += 1

    assert len(turn.player.hand) == 6
    assert len(turn.player.playmat) == 3
    assert turn.money == 3


def test_buy_copper(turn: Turn):
    assert turn.buys == 1
    assert len(turn.player.discard) == 0
    turn.buy(copper)
    assert turn.buys == 0
    assert len(turn.player.discard) == 1
    assert turn.money == 0


def test_buy_estate(turn: Turn):
    assert turn.buys == 1
    assert len(turn.player.discard) == 0
    turn.money = 3
    turn.buy(estate)
    assert turn.buys == 0
    assert len(turn.player.discard) == 1
    assert turn.money == 1


def test_buy_insufficient_buys(turn: Turn):
    turn.buy(copper)
    assert turn.buys == 0
    with pytest.raises(InsufficientBuys):
        turn.buy(copper)


def test_buy_insufficient_money(turn: Turn):
    with pytest.raises(InsufficientMoney):
        turn.buy(estate)
