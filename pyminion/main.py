from pyminion.models.core import (
    Game,
    Supply,
    Player,
    Deck,
    Trash,
)
from pyminion.expansions.base import (
    start_cards,
    core_supply,
    kingdom_cards,
)
from pyminion.models.base import (
    silver,
    gold,
    province,
)
from pyminion.bots.big_money import BigMoney
from pyminion.bots.bm_smithy import BM_Smithy
from pyminion.bots.human import Human


human = Human(deck=Deck(start_cards))
bm = BigMoney(deck=Deck(start_cards))
bm_smithy = BM_Smithy(deck=Deck(start_cards))

supply = Supply(piles=core_supply + kingdom_cards)
trash = Trash()
game = Game(players=[bm, human], supply=supply, trash=trash)

if __name__ == "__main__":
    game.start()
    while not game.is_over():

        bm.take_turn(game)
        human.take_turn(game)
        print(bm.deck)
        print(human.deck)

    winner = game.get_winner()
    print("Winner: ", winner.player_id)
    print("Turns: ", winner.turns)

    """
    with StringIO('yup') as f:
    stdin = sys.stdin
    sys.stdin = f
    print("'" + input() + "' wasn't actually typed at the command line")
    sys.stdin = stdin

    """
