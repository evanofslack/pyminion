from pyminion.bots import BigMoney
from pyminion.expansions.base import base_cards, basic_cards, chapel, start_cards
from pyminion.game import Game
from pyminion.players import Human

human = Human()
bot_1 = BigMoney(player_id="Bot 1")

players = [bot_1, human]
expansions = [base_cards]


game = Game(players, expansions, basic_cards, start_cards, kingdom_cards=[chapel])


if __name__ == "__main__":
    game.play()
    game.get_stats()
