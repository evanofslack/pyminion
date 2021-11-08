from pyminion.models.core import Player, Deck, Card
from pyminion.game import Game
from pyminion.exceptions import InvalidCardPlay

from typing import List, Optional


class Bot(Player):
    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "bot",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        for card in self.hand.cards:
            try:
                if card == target_card and card.type == "Action":
                    card.play(player=self, game=game, generic_play=generic_play)
                    return
            except Exception as e:
                print(e)
                raise InvalidCardPlay(
                    f"Invalid play, {target_card} could not be played"
                )
        raise InvalidCardPlay(f"Invalid play, {target_card} not in hand")

    def exact_play(self, card: Card, game: Game, generic_play: bool = True) -> None:
        try:
            if card.type == "Action":
                card.play(player=self, game=game, generic_play=generic_play)
            elif card.type == "Treasure":
                card.play(player=self, game=game)
        except:
            raise InvalidCardPlay(f"Invalid play, cannot play {card}")

    def binary_decision(self, card: Card) -> bool:
        if card.name == "Moneylender":
            return True
        else:
            return False

    def multiple_card_decision(
        self, card: Card, valid_cards: List[Card]
    ) -> Optional[List[Card]]:
        if card.name == "Cellar":
            return [
                card
                for card in valid_cards
                if card.name == "Estate" or card.name == "Copper"
            ]

    def single_card_decision(
        self, card: Card, valid_cards: List[Card]
    ) -> Optional[Card]:
        pass


class BigMoney(Bot):
    """
    Only buys money and provinces

    """

    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "big_money",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def take_turn(self, game: Game):

        if self.state.money >= 8:
            buy_card = "Province"
        elif self.state.money >= 6:
            buy_card = "Gold"
        elif self.state.money >= 3:
            buy_card = "Silver"
        else:
            buy_card = "\n"
