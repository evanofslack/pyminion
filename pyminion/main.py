from pyminion.models.core import (
    Game,
    Supply,
    Player,
    Deck,
    DiscardPile,
    Hand,
    Playmat,
    Turn,
    Trash,
)
from pyminion.expansions.base import (
    start_cards,
    core_supply,
    kingdom_cards,
)
from pyminion.models.base import estate, silver, moneylender, cellar, chapel


player_1 = Player(
    deck=Deck(start_cards),
    discard_pile=DiscardPile(),
    hand=Hand(),
    playmat=Playmat(),
    player_id="player_1",
)

supply = Supply(piles=core_supply + kingdom_cards)
trash = Trash()

game = Game(players=[player_1], supply=supply, trash=trash)

if __name__ == "__main__":

    turn = Turn(player=player_1)
    player_1.deck.shuffle()
    player_1.draw(5)
    player_1.hand.add(chapel)
    print(player_1.hand)
    player_1.hand.cards[-1].play(turn, player_1, trash)
    print(player_1.hand)
    print(player_1.playmat)
    print(player_1.discard_pile)
    print(trash)
    player_1.cleanup()

    """
    with StringIO('asdf') as f:
    stdin = sys.stdin
    sys.stdin = f
    print("'" + input() + "' wasn't actually typed at the command line")
    sys.stdin = stdin

    """
