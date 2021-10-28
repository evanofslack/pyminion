from pyminion.models.core import Player, Deck, Game
from pyminion.expansions.base import silver, gold, province, workshop, smithy
from pyminion.decisions import single_card_decision


class Human(Player):
    def __init__(
        self,
        deck: Deck,
        player_id: str = "human",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def choose_action(self, game: Game) -> bool:
        print(self.hand)
        card = single_card_decision(
            prompt="Choose an action card to play: ", valid_cards=self.hand.cards
        )
        if not card:
            return False
        self.play(card, game)
        print(f"{self.player_id} played {card}")

    def choose_buy(self, game: Game) -> bool:
        print("Money: ", self.state.money)
        card = single_card_decision(
            prompt="Choose a card to buy: ", valid_cards=game.supply.avaliable_cards()
        )
        if not card:
            return False
        self.buy(card, game.supply)
        print(f"{self.player_id} bought {card}")
        return True

    def take_turn(self, game: Game) -> None:
        self.start_turn()
        print("\nTurn: ", self.turns)
        play_actions = True
        while play_actions:
            play_actions = self.choose_action(game)
            if self.state.actions < 1:
                break
        self.autoplay_treasures()
        self.choose_buy(game)
        self.cleanup()
