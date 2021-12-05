from pyminion.bots.examples import BigMoney, BigMoneyUltimate
from pyminion.expansions.base import base_cards, smithy
from pyminion.game import Game
from pyminion.simulator import Simulator


def test_sim():
    bm = BigMoney()
    bm_ultimate = BigMoneyUltimate()
    game = Game(
        players=[bm, bm_ultimate], expansions=[base_cards], kingdom_cards=[smithy]
    )
    sim = Simulator(game, iterations=2)
    sim.run()
