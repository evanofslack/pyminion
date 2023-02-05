"""
Simulate multiple games between two or more bots.

"""
from pyminion.bots.examples import BigMoney, BigMoneySmithy
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game
from pyminion.simulator import Simulator

bm = BigMoney()
bm_smithy = BigMoneySmithy()


game = Game(
    players=[bm, bm_smithy],
    expansions=[base_set],
    kingdom_cards=[smithy],
    random_order=False,
    log_stdout=False,
    log_file=False,
)

sim = Simulator(game, iterations=1000)

if __name__ == "__main__":
    result = sim.run()
    print(result)
