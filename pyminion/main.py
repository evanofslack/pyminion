from pyminion.models.core import Game
from pyminion.expansions.base import (
    start_cards,
    base_cards,
    basic_cards,
)
from pyminion.players import BigMoney, Human

human = Human()
bot = BigMoney()

players = [bot, human]
expansions = [base_cards]


game = Game(
    players,
    expansions,
    basic_cards,
    start_cards,
)


if __name__ == "__main__":
    game.start()
    while not game.is_over():

        bot.take_turn(game)
        human.take_turn(game)

    print("\nWinner: ", game.get_winner())
    print("Turns: ", game.get_winner().turns)
