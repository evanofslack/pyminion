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
        if card.name == "Sentry":
            return False
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
                if card.name == "Copper"
                or "Victory" in card.type
                or "Curse" in card.type
            ]
        if card.name == "Poacher":

            discard_order = self.sort_for_discard(
                cards=valid_cards, actions=self.state.actions
            )

            return discard_order[:num_discard]

        if card.name == "Militia":

            discard_order = self.sort_for_discard(
                cards=valid_cards, actions=self.state.actions
            )

            return discard_order[:num_discard]

        if card.name == "Sentry":
            return [
                card
                for card in valid_cards
                if card.name == "Copper"
                or "Victory" in card.type
                or "Curse" in card.type
            ]

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

        if card.name == "Remodel":
            max_price_card = max(valid_cards, key=lambda card: card.cost)
            return max_price_card

        if card.name == "Mine":
            max_price_card = max(valid_cards, key=lambda card: card.cost)
            return max_price_card

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
        if card.name == "Remodel":
            min_price_card = min(valid_cards, key=lambda card: card.cost)
            return min_price_card

        if card.name == "Mine":
            min_price_card = min(valid_cards, key=lambda card: card.cost)
            return min_price_card

    def multiple_trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_trash: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:

        if card.name == "Chapel":
            trash_cards = self.determine_trash_cards(
                valid_cards=valid_cards, player=self, game=game
            )
            while len(trash_cards) > 4:
                trash_cards.pop()
            return trash_cards

        if card.name == "Sentry":
            return self.determine_trash_cards(
                valid_cards=valid_cards, player=self, game=game
            )

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

    def double_play_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if card.name == "Throne Room":
            # Double play most expensive card
            max_price_card = max(valid_cards, key=lambda card: card.cost)
            return max_price_card

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                return False
        return True

    @staticmethod
    def sort_for_discard(cards: List[Card], actions: int) -> List[Card]:
        """
        Sort list of cards from best discard candidate to worst discard candidate.
        First sort cards from lowest cost to highest cost. Then rearrange depending on remaining actions.
        If player has no remaining actions, prioritize discarding victory then action, then treasures.
        If player has remaining actions, prioritize discarding victory then treasure and action equally.

        """

        sorted_cards = sorted(cards, key=lambda card: card.cost)
        victory_cards = [
            card
            for card in sorted_cards
            if "Victory" in card.type or "Curse" in card.type
        ]
        non_victory_cards = [
            card
            for card in sorted_cards
            if "Victory" not in card.type or "Curse" not in card.type
        ]
        treasure_cards = [card for card in non_victory_cards if "Treasure" in card.type]
        action_cards = [
            card for card in non_victory_cards if "Treasure" not in card.type
        ]
        if actions == 0:
            return victory_cards + action_cards + treasure_cards
        else:
            return victory_cards + non_victory_cards

    def determine_trash_cards(
        self, valid_cards: List[Card], player: Player, game: "Game"
    ) -> List[Card]:
        """
        Determine which cards should be trashed.
        Trash Estate if number of provinces in supply >= 5
        Trash Copper if money in deck > 3 (keep enough to buy silver)
        Finally, sort the cards as to prioritize trashing estate over copper


        """
        deck_money = player.get_deck_money()
        trash_cards = []
        for card in valid_cards:
            if card.name == "Curse":
                trash_cards.append(card)
            elif (
                card.name == "Estate"
                and game.supply.pile_length(pile_name="Province") >= 5
            ):
                trash_cards.append(card)
            elif card.name == "Copper" and deck_money > 3:
                trash_cards.append(card)
                deck_money -= 1

        sorted_trash_cards = self.sort_for_discard(cards=trash_cards, actions=1)

        return sorted_trash_cards
