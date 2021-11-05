from pyminion.game import Game
from pyminion.simulator import Simulator
from pyminion.expansions.base import (
    start_cards,
    base_cards,
    basic_cards,
)
from pyminion.players import BigMoney, Human

human = Human()
bot_1 = BigMoney(player_id="Bot 1")
bot_2 = BigMoney(player_id="Bot 2")
bot_3 = BigMoney(player_id="Bot 3")
bot_4 = BigMoney(player_id="Bot 4")

players = [bot_1, bot_2]
expansions = [base_cards]


game = Game(
    players,
    expansions,
    basic_cards,
    start_cards,
)

sim = Simulator(game, iterations=100)

if __name__ == "__main__":
    sim.run()
    sim.get_stats()
