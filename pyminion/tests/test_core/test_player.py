from pyminion.models.core import Hand, DiscardPile, Player, Playmat, Turn, Supply
from pyminion.expansions.base import copper, estate
from pyminion.exceptions import InsufficientBuys, InsufficientMoney
import pytest


def test_create_player(deck):
    discard = DiscardPile()
    hand = Hand()
    playmat = Playmat()

    player = Player(deck=deck, discard=discard, hand=hand, playmat=playmat)
    assert len(player.deck) == 10
    assert len(player.discard) == 0
    assert len(player.hand) == 0
    assert len(player.playmat) == 0


def test_draw_normal(player: Player):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    player.draw()
    assert len(player.hand) == 1
    assert len(player.deck) == 9


def test_draw_empty_deck(player: Player):
    player.deck.move_to(player.discard)
    assert len(player.hand) == 0
    assert len(player.deck) == 0
    assert len(player.discard) == 10
    player.draw()
    assert len(player.deck) == 9
    assert len(player.hand) == 1
    assert len(player.discard) == 0


def test_draw_five(player: Player):
    assert len(player.hand) == 0
    player.draw_five()
    assert len(player.hand) == 5
    assert len(player.deck) == 5


def test_play_copper(player: Player, turn: Turn):
    player.hand.add(copper)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1


def test_autoplay_treasures(player: Player, turn: Turn):
    """
    Create a hand with 3 estates and 6 coppers. Play all coppers.
    Assert 6 coppers end up on playmat, 3 estates remain in hand,
    and that money increases to 6

    """
    for i in range(3):
        turn.player.hand.add(estate)
        turn.player.hand.add(copper)
        turn.player.hand.add(copper)
    assert len(player.hand) == 9

    player.autoplay_treasures(turn)

    assert len(player.hand) == 3
    assert len(player.playmat) == 6
    assert turn.money == 6


def test_buy_card_add_to_discard(turn: Turn, player: Player, supply: Supply):
    assert len(player.discard) == 0
    player.buy(copper, turn, supply)
    assert len(player.discard) == 1


def test_buy_card_remove_from_supply(turn: Turn, player: Player, supply: Supply):
    assert len(supply.piles[0]) == 8
    turn.money = 2
    player.buy(estate, turn, supply)
    assert len(supply.piles[0]) == 7


def test_buy_insufficient_buys(turn: Turn, player: Player, supply: Supply):
    player.buy(copper, turn, supply)
    assert turn.buys == 0
    with pytest.raises(InsufficientBuys):
        player.buy(copper, turn, supply)


def test_buy_insufficient_money(turn: Turn, player: Player, supply: Supply):
    with pytest.raises(InsufficientMoney):
        player.buy(estate, turn, supply)
