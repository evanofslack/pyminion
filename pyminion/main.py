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
    estate,
    silver,
    moneylender,
    cellar,
    chapel,
    copper,
    gold,
    province,
)


player = Player(
    deck=Deck(start_cards),
    player_id="player",
)
supply = Supply(piles=core_supply + kingdom_cards)
trash = Trash()
game = Game(players=[player], supply=supply, trash=trash)

if __name__ == "__main__":
    player.deck.shuffle()
    player.draw(5)

    while not game.is_over():
        player.start_turn()
        print(f"turns: {player.turns}")
        print(f"hand: {player.hand}")

        player.autoplay_treasures()
        print(f"money: {player.state.money}")
        if player.state.money >= 8:
            player.buy(province, supply)
        elif player.state.money >= 6:
            player.buy(gold, supply)
        elif player.state.money >= 3:
            player.buy(silver, supply)
        player.cleanup()

    """
    with StringIO('asdf') as f:
    stdin = sys.stdin
    sys.stdin = f
    print("'" + input() + "' wasn't actually typed at the command line")
    sys.stdin = stdin

    """
