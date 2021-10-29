from pyminion.models.core import (
    Game,
    Supply,
)
from pyminion.expansions.base import (
    start_deck,
    core_supply,
    kingdom_cards,
)
from pyminion.players import BigMoney, Human


human = Human(deck=start_deck)
bm = BigMoney(deck=start_deck)

supply = Supply(piles=core_supply + kingdom_cards)
game = Game(players=[bm, human], supply=supply)

if __name__ == "__main__":
    game.start()
    while not game.is_over():

        bm.take_turn(game)
        human.take_turn(game)

    print("\nWinner: ", game.get_winner())
    print("Turns: ", game.get_winner().turns)
