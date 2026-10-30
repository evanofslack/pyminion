import copy

from pyminion.bots.examples import BigMoney, BigMoneyUltimate
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game
from pyminion.simulator import Simulator


def test_sim():
    bm = BigMoney()
    bm_ultimate = BigMoneyUltimate()
    game = Game(
        players=[bm, bm_ultimate], expansions=[base_set], kingdom_cards=[smithy]
    )
    sim = Simulator(game, iterations=2)
    result = sim.run()

    assert "ran 2 games" in str(result)


def test_game_copy_isolates_state():
    bm = BigMoney()
    bm_ultimate = BigMoneyUltimate()
    game = Game(players=[bm, bm_ultimate], expansions=[base_set])
    game_copy = copy.copy(game)

    assert game_copy.players == game.players
    assert game_copy.players is not game.players
    assert game_copy.trash is not game.trash
    assert game_copy.effect_registry is not game.effect_registry


def test_sim_does_not_reorder_players():
    players = [BigMoney(player_id=str(i)) for i in range(4)]
    game = Game(players=players, expansions=[base_set], random_order=True, log_stdout=False)
    sim = Simulator(game, iterations=5)
    sim.run()

    assert game.players == players
