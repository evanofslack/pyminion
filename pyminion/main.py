from pyminion.models.core import Game, Supply, Deck
from pyminion.expansions.base import (
    start_cards,
    core_supply,
    kingdom_cards,
)
from pyminion.players import BigMoney, Human


human = Human(deck=Deck(start_cards))
bm = BigMoney(deck=Deck(start_cards))

supply = Supply(piles=core_supply + kingdom_cards)
game = Game(players=[bm, human], supply=supply)

if __name__ == "__main__":
    game.start()
    while not game.is_over():

        bm.take_turn(game)
        human.take_turn(game)

    print("\nWinner: ", game.get_winner())
    print("Turns: ", game.get_winner().turns)
