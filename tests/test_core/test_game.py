import pytest
from pyminion.bots import BigMoney, OptimizedBot
from pyminion.core import Card, Supply, Trash
from pyminion.exceptions import InvalidGameSetup, InvalidPlayerCount
from pyminion.expansions.base import base_cards, duchy, estate, gold, province, smithy
from pyminion.game import Game
from pyminion.players import Human


def test_game_fixture(game: Game):
    assert len(game.players) == 1
    assert isinstance(game.supply, Supply)
    assert isinstance(game.trash, Trash)
    assert not game.trash


def test_game_too_many_players(human: Human):
    with pytest.raises(InvalidPlayerCount):
        game = Game(players=[human, human, human, human, human], expansions=None)


def test_game_too_few_players():
    with pytest.raises(InvalidPlayerCount):
        game = Game(players=[], expansions=None)


def test_game_create_supply(game: Game):
    assert len(game.supply.piles) == 17


def test_setup_1_player(human: Human):
    game = Game(players=[human], expansions=[base_cards])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 10
    assert game.supply.pile_length(pile_name="Province") == 5
    assert game.supply.pile_length(pile_name="Copper") == 53


def test_setup_2_players(human: Human):
    game = Game(players=[human, human], expansions=[base_cards])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 10
    assert game.supply.pile_length(pile_name="Province") == 8
    assert game.supply.pile_length(pile_name="Copper") == 46


def test_setup_3_players(human: Human):
    game = Game(players=[human, human, human], expansions=[base_cards])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 20
    assert game.supply.pile_length(pile_name="Province") == 12
    assert game.supply.pile_length(pile_name="Copper") == 39


def test_setup_4_players(human: Human):
    game = Game(players=[human, human, human, human], expansions=[base_cards])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 30
    assert game.supply.pile_length(pile_name="Province") == 12
    assert game.supply.pile_length(pile_name="Copper") == 32


def test_setup_user_selected_card(human):
    game = Game(
        players=[human, human, human, human],
        expansions=[base_cards],
        kingdom_cards=[smithy],
    )
    game.supply = game._create_supply()
    assert smithy in game.supply.avaliable_cards()


def test_setup_invalid_user_selected_card(human):
    fake_card = Card(name="fake", cost=0, type=("Action",))
    game = Game(
        players=[human, human, human, human],
        expansions=[base_cards],
        kingdom_cards=[fake_card],
    )
    with pytest.raises(InvalidGameSetup):
        game.supply = game._create_supply()


def test_game_is_over_false(game: Game):
    assert not game.is_over()


def test_game_is_over_true_provinces(game: Game):
    # Single player game ony has 5 provinces
    for i in range(4):
        game.supply.gain_card(card=province)
    assert not game.is_over()
    game.supply.gain_card(card=province)
    assert game.is_over()


def test_game_is_over_true_three_piles(game: Game):
    for i in range(5):
        game.supply.gain_card(card=estate)
    assert not game.is_over()
    for i in range(5):
        game.supply.gain_card(card=duchy)
    assert not game.is_over()
    for i in range(29):
        game.supply.gain_card(card=gold)
    assert not game.is_over()
    game.supply.gain_card(card=gold)
    assert game.is_over()


def test_game_tie(multiplayer_game: Game):
    assert multiplayer_game.get_winner() is None


def test_game_win(multiplayer_game: Game):
    multiplayer_game.players[0].deck.add(estate)
    assert multiplayer_game.get_winner() == multiplayer_game.players[0]


def test_game_win_turns(multiplayer_game: Game):
    multiplayer_game.players[1].turns += 1
    assert multiplayer_game.get_winner() == multiplayer_game.players[0]


def test_game_1_player_play(bm_bot: BigMoney):
    game = Game(
        players=[bm_bot],
        expansions=[base_cards],
        kingdom_cards=[smithy],
        use_logger=False,
    )
    game.play()
    assert game.get_winner() == bm_bot


def test_game_2_player_play(bm_bot: BigMoney):
    game = Game(
        players=[bm_bot, bm_bot],
        expansions=[base_cards],
        kingdom_cards=[smithy],
        use_logger=False,
    )
    game.play()
    game.get_winner()
