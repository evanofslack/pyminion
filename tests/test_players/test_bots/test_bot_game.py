from pyminion.bots.examples import BigMoney, BigMoneyUltimate
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game


def test_game_single_player_play(bm_bot: BigMoney):
    # single player always wins by default
    game = Game(
        players=[bm_bot],
        expansions=[base_set],
        kingdom_cards=[smithy],
    )
    game.play()
    assert game.get_winners() == [bm_bot]


def test_game_2_player_play(bm_bot: BigMoney):
    game = Game(
        players=[bm_bot, bm_bot],
        expansions=[base_set],
        kingdom_cards=[smithy],
    )
    game.play()
    assert len(game.get_winners()) >= 1


def test_game_2_player_with_actions():
    bot = BigMoneyUltimate()
    game = Game(
        players=[bot, bot],
        expansions=[base_set],
        kingdom_cards=[smithy],
    )
    game.play()
    assert len(game.get_winners()) >= 1
