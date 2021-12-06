"""
Play a game through the terminal. Either by yourself, with another human, or against a bot. 

"""
from pyminion.bots.examples import BigMoney
from pyminion.expansions.base import base_set
from pyminion.game import Game
from pyminion.players import Human

human = Human(player_id="Human")
bot = BigMoney(player_id="Bot 1")

game = Game(players=[human, bot], expansions=[base_set])

if __name__ == "__main__":
    game.play()
