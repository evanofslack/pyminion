"""
Play a game through the terminal. Either by yourself, with another human, or against a bot. 

"""
from pyminion.bots import BigMoney
from pyminion.expansions.base import base_cards, basic_cards, start_cards
from pyminion.game import Game
from pyminion.players import Human

human = Human()
bot = BigMoney(player_id="Bot 1")

game = Game(
    players=[human, bot],
    expansions=[base_cards],
    basic_cards=basic_cards,
    start_cards=start_cards,
)

if __name__ == "__main__":
    game.play()
    game.get_stats()
