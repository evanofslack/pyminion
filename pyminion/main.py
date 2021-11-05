from pyminion.game import Game
from pyminion.expansions.base import (
    start_cards,
    base_cards,
    basic_cards,
)
from pyminion.players import BigMoney, Human

human = Human()
bot_1 = BigMoney(player_id="Bot 1")

players = [bot_1, human]
expansions = [base_cards]


game = Game(
    players,
    expansions,
    basic_cards,
    start_cards,
)


if __name__ == "__main__":
    game.play()
    game.get_stats()
