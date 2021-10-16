from pyminion.models.base import (
    Game,
    Supply,
    Player,
    Deck,
    DiscardPile,
    Hand,
    Playmat,
    Turn,
)
from pyminion.base_set.base_cards import start_cards, core_supply, silver


player_1 = Player(
    deck=Deck(start_cards),
    discard=DiscardPile(),
    hand=Hand(),
    playmat=Playmat(),
    player_id="player_1",
)

supply = Supply(piles=core_supply)

game = Game(players=[player_1], supply=supply)

if __name__ == "__main__":

    turn = Turn(player=player_1, game=game)

    player_1.deck.shuffle()
    player_1.draw_five()
    print(player_1.hand)
    print(player_1.deck)
    player_1.autoplay_treasures(turn)
    print(turn.money)
    player_1.buy(card=silver, turn=turn, supply=supply)
    print(player_1.discard)
