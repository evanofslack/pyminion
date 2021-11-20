import logging
from typing import List, Optional

from pyminion.exceptions import InvalidCardPlay
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

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        for card in self.hand.cards:
            try:
                if card.name == target_card.name and "Action" in card.type:
                    card.play(player=self, game=game, generic_play=generic_play)
                    return
            except Exception as e:
                logging.error(e)
                raise InvalidCardPlay(
                    f"Invalid play, {target_card} could not be played"
                )
        raise InvalidCardPlay(f"Invalid play, {target_card} not in hand")

    def exact_play(self, card: Card, game: Game, generic_play: bool = True) -> None:
        if "Action" in card.type:
            card.play(player=self, game=game, generic_play=generic_play)
        elif "Treasure" in card.type:
            card.play(player=self, game=game)

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

            # Add logic for playing action cards here

            return

    def start_treasure_phase(self, game: Game):
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        i = 0
        while i < len(viable_treasures):
            self.exact_play(viable_treasures[i], game)
            viable_treasures.remove(viable_treasures[i])
        logger.info(f"{self.player_id} has {self.state.money} money")

    def start_buy_phase(self, game: Game):
        while self.state.buys and self.state.money:

            # Add logic for buying cards here

            return

    def start_cleanup_phase(self):
        self.discard_pile.cards += self.hand.cards
        self.discard_pile.cards += self.playmat.cards
        self.hand.cards = []
        self.playmat.cards = []
        self.draw(5)

    def take_turn(self, game: Game) -> None:
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_turn()
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()