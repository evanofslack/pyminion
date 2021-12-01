"""
Simulate multiple games between two or more bots. 

"""
from pyminion.bots import BanditBot, BigMoney, BigMoneyUltimate, ChapelBot
from pyminion.expansions.base import base_cards, chapel, smithy
from pyminion.game import Game
from pyminion.players import Human
from pyminion.simulator import Simulator

bot_1 = BigMoneyUltimate()
bot_2 = ChapelBot()


game = Game(
    players=[bot_1, bot_2], expansions=[base_cards], kingdom_cards=[smithy, chapel]
)

sim = Simulator(game, iterations=1000)

if __name__ == "__main__":
    sim.run()
