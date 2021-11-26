import logging
from typing import TYPE_CHECKING, List, Optional

from pyminion.bots import Bot
from pyminion.core import Card
from pyminion.expansions.base import Estate, duchy, estate, silver
from pyminion.players import Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()


class OptimizedBot(Bot):
    """
    Bot with basic implementations for playing and reacting to all cards in the base set.

    """

    def __init__(
        self,
        player_id: str = "bot",
    ):
        super().__init__(player_id=player_id)

    def binary_resp(self, card: Card) -> bool:
        if card.name == "Moneylender":
            return True
        if card.name == "Vassal":
            return True
        else:
            return False

    def discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_discard: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:

        if card.name == "Cellar":
            return [
                card
                for card in valid_cards
                if card.name == "Copper" or "Victory" in card.type
            ]
        if card.name == "Poacher":
            sorted_cards = sorted(valid_cards, key=lambda card: card.cost)
            victory_cards = [card for card in sorted_cards if "Victory" in card.type]
            non_victory_cards = [
                card for card in sorted_cards if "Victory" not in card.type
            ]
            discard_order = victory_cards + non_victory_cards
            logger.info(discard_order)

            return discard_order[:num_discard]

    def gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:

        if card.name == "Artisan":
            if game.supply.pile_length(pile_name="Province") < 5:
                return duchy
            else:
                return silver

        if card.name == "Workshop":
            if game.supply.pile_length(pile_name="Province") < 3:
                return estate
            else:
                return silver

    def multiple_gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_gain: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        if required:
            return valid_cards[:num_gain]
        else:
            return None

    def trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Card:
        if required:
            return valid_cards[0]
        else:
            return None

    def multiple_trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_trash: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:

        if card.name == "Chapel":
            trash_cards = []
            deck_money = self.get_deck_money()
            for card in valid_cards:
                if (
                    game.supply.pile_length(pile_name="Province") >= 5
                    and card.name == "Estate"
                ):
                    trash_cards.append(card)
                if deck_money > 3 and card.name == "Copper":
                    trash_cards.append(card)
                    deck_money -= 1

            while len(trash_cards) > 4:
                trash_cards.pop()

            return trash_cards

    def topdeck_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:

        if card.name == "Artisan":
            for card in valid_cards:
                if "Action" in card.type and self.state.actions == 0:
                    return card
            else:
                return self.hand.cards[-1]

        if card.name == "Harbinger":
            # Do not topdeck victory cards
            best_topdeck = [card for card in valid_cards if "Victory" not in card.type]
            if not best_topdeck:
                return None
            # Topdeck highest price card if price > 2
            max_price_card = max(best_topdeck, key=lambda card: card.cost)
            if max_price_card.cost > 2:
                return max_price_card
            else:
                return None

        if card.name == "Bureaucrat":
            sorted_cards = sorted(valid_cards, key=lambda card: card.cost)
            return sorted_cards[0]

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                return False
        return True
