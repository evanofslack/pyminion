import pytest
from pyminion.core import AbstractDeck, DiscardPile, Hand, Playmat
from pyminion.exceptions import (
    CardNotFound,
    InsufficientActions,
    InsufficientBuys,
    InsufficientMoney,
    InvalidCardPlay,
)
from pyminion.expansions.base import (
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
from pyminion.expansions.alchemy import (
    alchemy_set,
    alchemist,
)
from pyminion.game import Game
from pyminion.player import Player
import pytest


def test_create_player(decider, deck):
    discard_pile = DiscardPile()
    hand = Hand()
    playmat = Playmat()

    player = Player(decider=decider, deck=deck, discard_pile=discard_pile, hand=hand, playmat=playmat)
    assert len(player.deck) == 10
    assert len(player.discard_pile) == 0
    assert len(player.hand) == 0
    assert len(player.playmat) == 0


def test_draw_normal(player: Player, game: Game):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    player.draw()
    assert len(player.hand) == 1
    assert len(player.deck) == 9


def test_draw_empty_deck(player: Player, game: Game):
    player.deck.move_to(player.discard_pile)
    assert len(player.hand) == 0
    assert len(player.deck) == 0
    assert len(player.discard_pile) == 10
    player.draw()
    assert len(player.deck) == 9
    assert len(player.hand) == 1
    assert len(player.discard_pile) == 0


def test_draw_empty_deck_empty_discard_pile(player: Player, game: Game):
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


def test_draw_multiple(player: Player, game: Game):
    assert len(player.hand) == 0
    assert len(player.deck) == 10
    player.draw(num_cards=3)
    assert len(player.hand) == 3
    assert len(player.deck) == 7


def test_play_copper(player: Player, game: Game):
    player.hand.add(copper)
    assert len(player.hand) == 1
    player.play(copper, game)
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
    with pytest.raises(CardNotFound):
        player.play(target_card=smithy, game=game)


def test_buy_card_add_to_discard_pile(player: Player, game: Game):
    assert len(player.discard_pile) == 0
    player.buy(copper, game)
    assert len(player.discard_pile) == 1


def test_buy_card_remove_from_supply(player: Player, multiplayer_game: Game):
    assert len(multiplayer_game.supply.get_pile("Estate")) == 8
    player.state.money = 2
    player.buy(estate, multiplayer_game)
    assert len(multiplayer_game.supply.get_pile("Estate")) == 7


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([alchemist])
def test_buy_potions(player: Player, game: Game):
    player.state.money = 3
    player.state.potions = 1
    player.buy(alchemist, game)
    assert player.state.money == 0
    assert player.state.potions == 0
    assert len(player.discard_pile) == 1
    assert player.discard_pile.cards[0].name == "Alchemist"
    assert len(game.supply.get_pile("Alchemist")) == 9


def test_buy_insufficient_buys(player: Player, game: Game):
    player.buy(copper, game)
    assert player.state.buys == 0
    with pytest.raises(InsufficientBuys):
        player.buy(copper, game)


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([alchemist])
def test_buy_insufficient_money(player: Player, game: Game):
    with pytest.raises(InsufficientMoney):
        player.buy(estate, game)

    player.state.money = 3
    with pytest.raises(InsufficientMoney):
        player.buy(alchemist, game)


def test_player_trash(player: Player, game: Game):
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(game.trash) == 0
    assert len(player.hand) == 2
    player.trash(copper, game)
    assert len(player.hand) == 1
    assert type(player.hand.cards[0]) is Estate
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is Copper


def test_player_discard(player: Player, game: Game):
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(player.discard_pile) == 0
    assert len(player.hand) == 2
    player.discard(game, copper)
    assert len(player.hand) == 1
    assert type(player.hand.cards[0]) is Estate
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is Copper


def test_player_all_cards(player: Player):
    assert player.get_all_cards_count() == 10
    player.hand.add(copper)
    assert player.get_all_cards_count() == 11
    player.discard_pile.add(copper)
    assert player.get_all_cards_count() == 12
    player.deck.add(copper)
    assert player.get_all_cards_count() == 13
    player.playmat.add(copper)
    assert player.get_all_cards_count() == 14
    player.playmat.remove(copper)
    assert player.get_all_cards_count() == 13
    player.get_mat("test").add(copper)
    assert player.get_all_cards_count() == 14
    player.set_aside.add(copper)
    assert player.get_all_cards_count() == 15


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
    player.play(copper, game)
    assert player.state.money == 1


def test_play_action_decrement_action(player: Player, game: Game):
    player.hand.add(smithy)
    assert player.state.actions == 1
    player.play(smithy, game)
    assert player.state.actions == 0


def test_insufficient_actions(player: Player, game: Game):
    player.hand.add(smithy)
    player.hand.add(smithy)
    player.play(smithy, game)
    assert player.state.actions == 0
    with pytest.raises(InsufficientActions):
        player.play(smithy, game)


def test_player_gain_card(player: Player, game: Game):
    player.gain(card=copper, game=game)
    assert player.discard_pile.cards[0] == copper
    assert len(player.discard_pile) == 1


def test_player_try_gain_card(player: Player, game: Game):
    copper_pile = game.supply.get_pile("Copper")
    copper_pile.cards = copper_pile.cards[:3]
    assert len(copper_pile) == 3

    dest = AbstractDeck()
    for _ in range(5):
        player.try_gain(copper, game, destination=dest)

    assert len(copper_pile) == 0
    assert len(dest) == 3


def test_player_draw_to_discard(player: Player, game: Game):
    assert len(player.discard_pile) == 0
    player.draw(num_cards=1, destination=player.discard_pile)
    assert len(player.discard_pile) == 1


def test_shuffle_count(player: Player, game: Game):
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
    assert player.get_all_cards_count() == 10
    player.hand.add(copper)
    player.discard_pile.add(copper)
    assert player.get_all_cards_count() == 12


def test_card_count(player: Player):
    assert player.get_card_count(card=copper) == 7
    assert player.get_card_count(card=estate) == 3
    assert player.get_card_count(card=smithy) == 0
    player.hand.add(smithy)
    assert player.get_card_count(card=smithy) == 1


def test_start_turn(player: Player, game: Game):
    player.turns = 2
    player.state.money = 2
    player.state.actions = 2
    player.state.buys = 2
    player.start_turn(game)
    assert player.turns == 3
    assert player.state.money == 0
    assert player.state.potions == 0
    assert player.state.actions == 1
    assert player.state.buys == 1


def test_cleanup_phase(player: Player, game: Game):
    player.hand.add(copper)
    player.playmat.add(copper)
    player.start_cleanup_phase(game)
    assert len(player.hand) == 5
    assert len(player.playmat) == 0
