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
    estate,
    silver,
    moneylender,
)


player_1 = Player(
    deck=Deck(start_cards),
    discard=DiscardPile(),
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
    player_1.autoplay_treasures(turn)
    if turn.money > 2:
        player_1.buy(card=silver, turn=turn, supply=supply)
    player_1.cleanup()

    turn = Turn(player=player_1)
    player_1.draw(5)
    player_1.hand.add(moneylender)
    print(player_1.hand)
    print(player_1.playmat)
    print(player_1.discard)
    player_1.hand.cards[-1].play(turn, player_1, trash)
    print(game.trash)
    print(trash)
    print(turn.money)

    """
    with StringIO('asdf') as f:
    stdin = sys.stdin
    sys.stdin = f
    print("'" + input() + "' wasn't actually typed at the command line")
    sys.stdin = stdin

    """
