import pytest
from pyminion.exceptions import (
    InsufficientActions,
    InsufficientBuys,
    InsufficientMoney,
    InvalidCardPlay,
)
from pyminion.game import Game
from pyminion.models.base import (
    Copper,
    Estate,
    copper,
    duchy,
    estate,
    gardens,
    market,
    poacher,
    province,
    smithy,
    vassal,
)
from pyminion.models.core import DiscardPile, Hand, Player, Playmat, Supply, Trash


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
    assert null is None
    assert len(player.hand) == 10
    assert len(player.deck) == 0
    assert len(player.discard_pile) == 0


def test_draw_multiple(player: Player):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    player.draw(num_cards=3)
    assert len(player.hand) == 3
    assert len(player.deck) == 7


def test_play_copper(player: Player, game: Game):
    player.hand.add(copper)
    assert len(player.hand) == 1
    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1


def test_player_play_valid(player: Player, game: Game):
    player.hand.add(smithy)
    player.play(target_card=smithy, game=game)
    assert len(player.playmat) == 1
    assert len(player.hand) == 3


def test_player_play_invalid_play(player: Player, game: Game):
    player.hand.add(estate)
    with pytest.raises(InvalidCardPlay):
        player.play(target_card=estate, game=game)


def test_player_play_not_in_hand(player: Player, game: Game):
    with pytest.raises(InvalidCardPlay):
        player.play(target_card=smithy, game=game)


def test_buy_card_add_to_discard_pile(player: Player, supply: Supply):
    assert len(player.discard_pile) == 0
    player.buy(copper, supply)
    assert len(player.discard_pile) == 1


def test_buy_card_remove_from_supply(player: Player, supply: Supply):
    assert len(supply.piles[0]) == 8
    player.state.money = 2
    player.buy(estate, supply)
    assert len(supply.piles[0]) == 7


def test_buy_insufficient_buys(player: Player, supply: Supply):
    player.buy(copper, supply)
    assert player.state.buys == 0
    with pytest.raises(InsufficientBuys):
        player.buy(copper, supply)


def test_buy_insufficient_money(player: Player, supply: Supply):
    with pytest.raises(InsufficientMoney):
        player.buy(estate, supply)


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


def test_player_discard(player: Player):
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(player.discard_pile) == 0
    assert len(player.hand) == 2
    player.discard(copper)
    assert len(player.hand) == 1
    assert type(player.hand.cards[0]) is Estate
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is Copper


def test_player_all_cards(player: Player):
    assert len(player.get_all_cards()) == 10
    player.hand.add(copper)
    assert len(player.get_all_cards()) == 11
    assert type(player.get_all_cards()) is list
    player.discard_pile.add(copper)
    assert len(player.get_all_cards()) == 12
    player.deck.add(copper)
    assert len(player.get_all_cards()) == 13
    player.playmat.add(copper)
    assert len(player.get_all_cards()) == 14
    player.playmat.remove(copper)
    assert len(player.get_all_cards()) == 13


def test_player_get_vp(player: Player):
    assert player.get_victory_points() == 3
    player.hand.add(estate)
    assert player.get_victory_points() == 4
    player.hand.add(duchy)
    assert player.get_victory_points() == 7
    player.hand.add(province)
    assert player.get_victory_points() == 13
    player.hand.add(gardens)
    assert player.get_victory_points() == 14


def test_play_treasure_increment_money(player: Player, game: Game):
    player.hand.add(copper)
    assert player.state.money == 0
    player.hand.cards[0].play(player, game)
    assert player.state.money == 1


def test_play_action_decrement_action(player: Player, game: Game):
    player.hand.add(smithy)
    assert player.state.actions == 1
    player.hand.cards[0].play(player, game)
    assert player.state.actions == 0


def test_insufficient_actions(player: Player, game: Game):
    player.hand.add(smithy)
    player.hand.add(smithy)
    player.hand.cards[0].play(player, game)
    assert player.state.actions == 0
    with pytest.raises(InsufficientActions):
        player.hand.cards[0].play(player, game)


def test_player_gain_card(player: Player, supply: Supply):
    player.gain(card=copper, supply=supply)
    assert player.discard_pile.cards[0] == copper
    assert len(player.discard_pile) == 1


def test_player_draw_to_discard(player: Player):
    assert len(player.discard_pile) == 0
    player.draw(num_cards=1, destination=player.discard_pile)
    assert len(player.discard_pile) == 1


def test_shuffle_count(player: Player):
    assert player.shuffles == 0
    player.discard_pile.add(copper)
    player.draw(11)
    assert player.shuffles == 1
    player.discard_pile.add(copper)
    player.draw(1)
    assert player.shuffles == 2


def test_treasure_money(player: Player):
    assert player.get_treasure_money() == 7
    player.deck.add(copper)
    assert player.get_treasure_money() == 8


def test_action_money(player: Player):
    assert player.get_action_money() == 0
    player.deck.add(copper)
    assert player.get_action_money() == 0
    player.deck.add(vassal)
    assert player.get_action_money() == 2
    player.hand.add(market)
    assert player.get_action_money() == 3
    player.discard_pile.add(poacher)
    assert player.get_action_money() == 4


def test_deck_money(player: Player):
    assert player.get_deck_money() == 7
    player.hand.add(copper)
    player.deck.add(vassal)
    assert player.get_deck_money() == 10


def test_all_cards(player: Player):
    assert len(player.get_all_cards()) == 10
    player.hand.add(copper)
    player.discard_pile.add(copper)
    assert len(player.get_all_cards()) == 12


def test_card_count(player: Player):
    assert player.get_card_count(card=copper) == 7
    assert player.get_card_count(card=estate) == 3
    assert player.get_card_count(card=smithy) == 0
    player.hand.add(smithy)
    assert player.get_card_count(card=smithy) == 1
