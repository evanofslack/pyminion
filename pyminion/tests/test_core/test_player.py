from pyminion.models.core import Hand, DiscardPile, Player, Playmat, Turn, Supply, Trash
from pyminion.models.base import Estate, Copper, copper, estate
from pyminion.exceptions import InsufficientBuys, InsufficientMoney
import pytest


def test_create_player(deck):
    discard_pile = DiscardPile()
    hand = Hand()
    playmat = Playmat()

    player = Player(deck=deck, discard_pile=discard_pile, hand=hand, playmat=playmat)
    assert len(player.deck) == 10
    assert len(player.discard_pile) == 0
    assert len(player.hand) == 0
    assert len(player.playmat) == 0


def test_draw_normal(player: Player):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    player.draw()
    assert len(player.hand) == 1
    assert len(player.deck) == 9


def test_draw_empty_deck(player: Player):
    player.deck.move_to(player.discard_pile)
    assert len(player.hand) == 0
    assert len(player.deck) == 0
    assert len(player.discard_pile) == 10
    player.draw()
    assert len(player.deck) == 9
    assert len(player.hand) == 1
    assert len(player.discard_pile) == 0


def test_draw_empty_deck_empty_discard_pile(player: Player):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    assert len(player.discard_pile) == 0
    player.draw(10)
    assert len(player.hand) == 10
    assert len(player.deck) == 0
    assert len(player.discard_pile) == 0
    null = player.draw()
    assert null == None
    assert len(player.hand) == 10
    assert len(player.deck) == 0
    assert len(player.discard_pile) == 0


def test_draw_multiple(player: Player):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    player.draw(num_cards=3)
    assert len(player.hand) == 3
    assert len(player.deck) == 7


def test_play_copper(player: Player, turn: Turn):
    player.hand.add(copper)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1


def test_autoplay_treasures(player: Player, turn: Turn):
    for i in range(3):
        turn.player.hand.add(estate)
        turn.player.hand.add(copper)
        turn.player.hand.add(copper)
    assert len(player.hand) == 9

    player.autoplay_treasures(turn)

    assert len(player.hand) == 3
    assert len(player.playmat) == 6
    assert turn.money == 6


def test_buy_card_add_to_discard_pile(turn: Turn, player: Player, supply: Supply):
    assert len(player.discard_pile) == 0
    player.buy(copper, turn, supply)
    assert len(player.discard_pile) == 1


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


def test_player_cleanup(turn: Turn, player: Player):
    player.draw(5)
    assert len(player.hand) == 5
    assert len(player.discard_pile) == 0
    assert len(player.playmat) == 0
    player.autoplay_treasures(turn)
    assert len(player.playmat) > 0
    player.cleanup()
    assert len(player.discard_pile) == 5
    assert len(player.hand) == 0
    assert len(player.playmat) == 0


def test_player_trash(player: Player, trash: Trash):
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(trash) == 0
    assert len(player.hand) == 2
    player.trash(copper, trash)
    assert len(player.hand) == 1
    assert type(player.hand.cards[0]) is Estate
    assert len(trash) == 1
    assert type(trash.cards[0]) is Copper


def test_player_discard_pile(player: Player):
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(player.discard_pile) == 0
    assert len(player.hand) == 2
    player.discard(copper)
    assert len(player.hand) == 1
    assert type(player.hand.cards[0]) is Estate
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is Copper
