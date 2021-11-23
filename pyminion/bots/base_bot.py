import logging
from typing import Iterator, List, Optional

from pyminion.exceptions import CardNotFound, EmptyPile, InvalidCardPlay
from pyminion.game import Game
from pyminion.models.core import Card, Deck, Player

logger = logging.getLogger()


class Bot(Player):
    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "bot",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def discard_decision(self, card: Card, valid_cards: List[Card]) -> Card:
        pass

    def gain_decision(self, card: Card, valid_cards: List[Card]) -> Card:
        pass

    def trash_decision(self, card: Card, valid_cards: List[Card]) -> Card:
        pass

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

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                return False
        return True

    def start_action_phase(self, game: Game):
        viable_actions = [card for card in self.hand.cards if "Action" in card.type]
        logger.info(f"{self.player_id}'s hand: {self.hand}")
        while viable_actions and self.state.actions:
            for card in self.action_priority(game=game):
                try:
                    self.play(target_card=card, game=game)
                except CardNotFound:
                    pass
            return

    def start_treasure_phase(self, game: Game):
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        i = 0
        while i < len(viable_treasures):
            self.exact_play(viable_treasures[i], game)
            viable_treasures.remove(viable_treasures[i])
        logger.info(f"{self.player_id} has {self.state.money} money")

    def start_buy_phase(self, game: Game):
        while self.state.buys:
            for card in self.buy_priority(game=game):
                try:
                    self.buy(card, supply=game.supply)
                    return
                except EmptyPile:
                    pass
            else:
                logger.info(f"{self} buys nothing")
                return

    def take_turn(self, game: Game) -> None:
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_turn()
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()

    def action_priority(self, game: Game) -> Iterator[Card]:
        """
        Add logic for playing action cards here

        """
        pass

    def buy_priority(self, game: Game) -> Iterator[Card]:
        """
        Add logic for buy priority here

        """
        pass
