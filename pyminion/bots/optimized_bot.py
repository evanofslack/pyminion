import logging
from typing import TYPE_CHECKING, List, Optional, Union

from pyminion.bots.bot import Bot
from pyminion.core import Card
from pyminion.exceptions import InvalidBotImplementation
from pyminion.expansions.base import duchy, estate, silver
from pyminion.players import Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()


class OptimizedBot(Bot):
    """
    Implements opinionated logic for playing and reacting to all cards in the base set.

    The intention is to inherit from this class to make concrete bot implementations.
    If inheriting from this bot, it is possible to change the way that a single card is executed
    by overwriting the card specific method at the bottom of this file.


    """

    def __init__(
        self,
        player_id: str = "bot",
    ):
        super().__init__(player_id=player_id)

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
            if "Victory" not in card.type and "Curse" not in card.type
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
        Determine which cards should be trashed:

        Always trash Curse
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

    def binary_resp(
        self, card: Card, game: "Game", relevant_cards: Optional[List[Card]] = None
    ) -> bool:
        if card.name == "Moneylender":
            return self.moneylender()
        if card.name == "Vassal":
            return self.vassal(relevant_cards=relevant_cards)
        if card.name == "Sentry":
            return self.sentry(game=game, relevant_cards=relevant_cards, binary=True)
        if card.name == "Library":
            return self.library(relevant_cards=relevant_cards)
        else:
            return True

    def discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        return super().discard_resp(
            card=card, valid_cards=valid_cards, game=game, required=required
        )

    def multiple_discard_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_discard: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:

        if card.name == "Cellar":
            return self.cellar(valid_cards=valid_cards)
        if card.name == "Poacher":
            return self.poacher(valid_cards=valid_cards, num_discard=num_discard)

        if card.name == "Militia":
            return self.militia(valid_cards=valid_cards, num_discard=num_discard)

        if card.name == "Sentry":
            return self.sentry(game=game, valid_cards=valid_cards, discard=True)

    def gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:

        if card.name == "Artisan":
            return self.artisan(game=game, gain=True)
        if card.name == "Workshop":
            return self.workshop(game=game)
        if card.name == "Remodel":
            return self.remodel(valid_cards=valid_cards, gain=True)
        if card.name == "Mine":
            return self.mine(valid_cards=valid_cards, gain=True)

    def multiple_gain_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_gain: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:
        return super().multiple_gain_resp(
            card=card,
            valid_cards=valid_cards,
            game=game,
            num_gain=num_gain,
            required=required,
        )

    def trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if card.name == "Remodel":
            return self.remodel(valid_cards=valid_cards, trash=True)
        if card.name == "Mine":
            return self.mine(valid_cards=valid_cards, trash=True)

    def multiple_trash_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        num_trash: Optional[int] = None,
        required: bool = True,
    ) -> Optional[List[Card]]:

        if card.name == "Chapel":
            return self.chapel(game=game, valid_cards=valid_cards)
        if card.name == "Sentry":
            return self.sentry(game=game, valid_cards=valid_cards, trash=True)

    def topdeck_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:

        if card.name == "Artisan":
            return self.artisan(game=game, valid_cards=valid_cards, topdeck=True)
        if card.name == "Harbinger":
            return self.harbinger(valid_cards=valid_cards)

        if card.name == "Bureaucrat":
            return self.bureaucrat(valid_cards=valid_cards)

    def double_play_resp(
        self,
        card: Card,
        valid_cards: List[Card],
        game: "Game",
        required: bool = True,
    ) -> Optional[Card]:
        if card.name == "Throne Room":
            return self.throne_room(valid_cards=valid_cards)

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                return False
        return True

    # CARD SPECIFIC IMPLEMENTATIONS
    def moneylender(self) -> bool:
        return True

    def vassal(self, relevant_cards: Optional[List[Card]]) -> bool:
        return True

    def library(self, relevant_cards: Optional[List[Card]]) -> bool:
        if self.state.actions == 0:
            return True
        else:
            return False

    def sentry(
        self,
        game: "Game",
        valid_cards: Optional[List[Card]] = None,
        relevant_cards: Optional[List[Card]] = None,
        trash: bool = False,
        discard: bool = False,
        binary: bool = False,
    ) -> Union[List[Card], bool]:
        if trash:
            if not valid_cards:
                return []
            return self.determine_trash_cards(
                valid_cards=valid_cards, player=self, game=game
            )
        if discard:
            if not valid_cards:
                return []
            return [
                card
                for card in valid_cards
                if card.name == "Copper"
                or "Victory" in card.type
                or "Curse" in card.type
            ]
        if binary:
            return False

        raise InvalidBotImplementation(
            "Either gain, topdeck or binary must be true when playing sentry"
        )

    def cellar(self, valid_cards: List[Card]) -> Optional[List[Card]]:
        return [
            card
            for card in valid_cards
            if card.name == "Copper" or "Victory" in card.type or "Curse" in card.type
        ]

    def poacher(
        self, valid_cards: List[Card], num_discard: Optional[int]
    ) -> List[Card]:
        if not num_discard:
            return []
        discard_order = self.sort_for_discard(
            cards=valid_cards, actions=self.state.actions
        )
        return discard_order[:num_discard]

    def militia(
        self, valid_cards: List[Card], num_discard: Optional[int]
    ) -> List[Card]:
        if not num_discard:
            return []
        discard_order = self.sort_for_discard(
            cards=valid_cards, actions=self.state.actions
        )
        return discard_order[:num_discard]

    def artisan(
        self,
        game: "Game",
        valid_cards: Optional[List[Card]] = None,
        gain: bool = False,
        topdeck: bool = False,
    ) -> Card:
        if topdeck:
            for card in self.hand.cards:
                if "Action" in card.type and self.state.actions == 0:
                    return card
            else:
                return self.hand.cards[-1]
        if gain:
            if game.supply.pile_length(pile_name="Province") < 5:
                return duchy
            else:
                return silver

        raise InvalidBotImplementation(
            "Either gain or topdeck must be true when playing artisian"
        )

    def workshop(self, game: "Game") -> Card:
        if game.supply.pile_length(pile_name="Province") < 3:
            return estate
        else:
            return silver

    def remodel(
        self, valid_cards: List[Card], trash: bool = False, gain: bool = False
    ) -> Card:
        if trash:
            min_price_card = min(valid_cards, key=lambda card: card.cost)
            return min_price_card

        if gain:
            max_price_card = max(valid_cards, key=lambda card: card.cost)
            return max_price_card

        raise InvalidBotImplementation(
            "Either gain or trash must be true when playing remodel"
        )

    def mine(
        self, valid_cards: List[Card], trash: bool = False, gain: bool = False
    ) -> Card:
        if trash:
            min_price_card = min(valid_cards, key=lambda card: card.cost)
            return min_price_card

        if gain:
            max_price_card = max(valid_cards, key=lambda card: card.cost)
            return max_price_card

        raise InvalidBotImplementation(
            "Either gain or trash must be true when playing mine"
        )

    def chapel(self, game: "Game", valid_cards: List[Card]) -> Optional[List[Card]]:
        trash_cards = self.determine_trash_cards(
            valid_cards=valid_cards, player=self, game=game
        )
        while len(trash_cards) > 4:
            trash_cards.pop()
        return trash_cards

    def harbinger(self, valid_cards: List[Card]) -> Optional[Card]:
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

    def bureaucrat(self, valid_cards: List[Card]) -> Card:
        sorted_cards = sorted(valid_cards, key=lambda card: card.cost)
        return sorted_cards[0]

    def throne_room(self, valid_cards: List[Card]) -> Card:
        # Double play most expensive card
        max_price_card = max(valid_cards, key=lambda card: card.cost)
        return max_price_card
