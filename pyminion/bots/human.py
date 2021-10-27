from pyminion.models.core import Player, Deck, Game
from pyminion.expansions.base import silver, gold, province


class Human(Player):
    def __init__(
        self,
        deck: Deck,
        player_id: str = "human",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def take_turn(self, game: Game):
        self.start_turn()
        print(f"bot turns: {self.turns}")

        self.autoplay_treasures()
        print(f"bot money: {self.state.money}")
        if self.state.money >= 8:
            self.buy(province, game.supply)
        elif self.state.money >= 6:
            self.buy(gold, game.supply)
        elif self.state.money >= 3:
            self.buy(silver, game.supply)
        self.cleanup()
