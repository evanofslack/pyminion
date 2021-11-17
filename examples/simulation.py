from pyminion.bots.big_money import BigMoney
from pyminion.bots.big_money_ultimate import BigMoneyUltimate
from pyminion.expansions.base import base_cards, basic_cards, smithy, start_cards
from pyminion.game import Game
from pyminion.players import Human
from pyminion.simulator import Simulator

human = Human()
bot_1 = BigMoney(player_id="Big Money")
bot_2 = BigMoneyUltimate(player_id="Big Money Ultimate")


players = [bot_1, bot_2]
expansions = [base_cards]


game = Game(players, expansions, basic_cards, start_cards, kingdom_cards=[smithy])

sim = Simulator(game, iterations=1000)

if __name__ == "__main__":
    sim.run()
    sim.get_stats()
