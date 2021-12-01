"""
Run a single game between two bots. 

"""
from logging import log

from pyminion.bots import BigMoney, BigMoneyUltimate
from pyminion.expansions.base import base_cards, smithy
from pyminion.game import Game

bot_1 = BigMoney(player_id="Bot 1")
bot_2 = BigMoneyUltimate(player_id="Bot 2")


players = [bot_1, bot_2]
expansions = [base_cards]

game = Game(
    players=[bot_1, bot_2],
    expansions=[base_cards],
    kingdom_cards=[smithy],
)

if __name__ == "__main__":
    game.play()
