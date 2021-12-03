"""
Simulate multiple games between two or more bots. 

"""
from pyminion.bots import (
    BanditBot,
    BigMoney,
    BigMoneySmithy,
    BigMoneyUltimate,
    ChapelBot,
)
from pyminion.expansions.base import bandit, base_cards, smithy
from pyminion.game import Game
from pyminion.players import Human
from pyminion.simulator import Simulator

bot_1 = BigMoney()
bot_2 = BigMoneySmithy()


game = Game(
    players=[bot_1, bot_2], expansions=[base_cards], kingdom_cards=[smithy, bandit]
)

sim = Simulator(game, iterations=1000)

if __name__ == "__main__":
    sim.run()
