from pyminion.game import Game
from pyminion.simulator import Simulator
from pyminion.examples.bot_game import game

sim = Simulator(game, iterations=100)

if __name__ == "__main__":
    sim.run()
    sim.get_stats()
