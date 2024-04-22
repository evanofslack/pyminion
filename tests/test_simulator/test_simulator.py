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
