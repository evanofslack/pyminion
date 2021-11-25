from pyminion.core import Supply, Trash
from pyminion.expansions.base import duchy, estate, gold, province
from pyminion.game import Game


def test_game_fixture(game: Game):
    assert len(game.players) == 1
    assert isinstance(game.supply, Supply)
    assert isinstance(game.trash, Trash)
    assert not game.trash


def test_game_create_supply(game: Game):
    assert len(game.supply.piles) == 17


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
