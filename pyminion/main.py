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


player = Player(
    deck=Deck(start_cards),
    player_id="player",
)
bm = BigMoney(deck=Deck(start_cards))
bm_smithy = BM_Smithy(deck=Deck(start_cards))

supply = Supply(piles=core_supply + kingdom_cards)
trash = Trash()
game = Game(players=[bm, bm_smithy], supply=supply, trash=trash)

if __name__ == "__main__":

    bm.deck.shuffle()
    bm.draw(5)
    bm_smithy.deck.shuffle()
    bm_smithy.draw(5)
    while not game.is_over():

        bm.take_turn(game)
        bm_smithy.take_turn(game)

    winner = game.get_winner()
    print(winner.player_id)

    """
    with StringIO('yup') as f:
    stdin = sys.stdin
    sys.stdin = f
    print("'" + input() + "' wasn't actually typed at the command line")
    sys.stdin = stdin

    """
