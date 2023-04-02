import logging
from typing import TYPE_CHECKING, List, Optional, Union

from pyminion.bots.bot import Bot
from pyminion.core import CardType, Card
from pyminion.exceptions import InvalidBotImplementation
from pyminion.expansions.base import duchy, estate, silver
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game

logger = logging.getLogger()


class OptimizedBotDecider:
    """
    Optimized representation of Bot decision making.

    """

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
            if CardType.Victory in card.type or CardType.Curse in card.type
        ]
        non_victory_cards = [
            card
            for card in sorted_cards
            if CardType.Victory not in card.type and CardType.Curse not in card.type
        ]
        treasure_cards = [card for card in non_victory_cards if CardType.Treasure in card.type]
        action_cards = [
            card for card in non_victory_cards if CardType.Treasure not in card.type
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
            if card.name == CardType.Curse:
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

    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List[Card]] = None,
    ) -> bool:
        if card.name == "Moneylender":
            return self.moneylender(player=player)
        elif card.name == "Vassal":
            return self.vassal(player=player, relevant_cards=relevant_cards)
        elif card.name == "Sentry":
            return self.sentry(player=player, game=game, relevant_cards=relevant_cards, binary=True)
        elif card.name == "Library":
            return self.library(player=player, relevant_cards=relevant_cards)
        else:
            return True

    def discard_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_discard: int = 0,
        max_num_discard: int = -1,
    ) -> List["Card"]:
        if card.name == "Cellar":
            return self.cellar(player=player, valid_cards=valid_cards)
        elif card.name == "Poacher":
            return self.poacher(player=player, valid_cards=valid_cards, num_discard=min_num_discard)
        elif card.name == "Militia":
            return self.militia(player=player, valid_cards=valid_cards, num_discard=min_num_discard)
        elif card.name == "Sentry":
            return self.sentry(player=player, game=game, valid_cards=valid_cards, discard=True)
        else:
            return valid_cards[:min_num_discard]

    def trash_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_trash: int = 0,
        max_num_trash: int = -1,
    ) -> List["Card"]:
        if card.name == "Remodel":
            ret = self.remodel(player=player, valid_cards=valid_cards, trash=True)
            return [ret]
        elif card.name == "Mine":
            ret = self.mine(player=player, valid_cards=valid_cards, trash=True)
            return [ret]
        elif card.name == "Chapel":
            return self.chapel(player=player, game=game, valid_cards=valid_cards)
        elif card.name == "Sentry":
            return self.sentry(player=player, game=game, valid_cards=valid_cards, trash=True)
        else:
            return valid_cards[:min_num_trash]

    def gain_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_gain: int = 0,
        max_num_gain: int = -1,
    ) -> List["Card"]:
        if card.name == "Artisan":
            ret = self.artisan(player=player, game=game, gain=True)
            return [ret]
        elif card.name == "Workshop":
            ret = self.workshop(player=player, game=game)
            return [ret]
        elif card.name == "Remodel":
            ret = self.remodel(player=player, valid_cards=valid_cards, gain=True)
            return [ret]
        elif card.name == "Mine":
            ret = self.mine(player=player, valid_cards=valid_cards, gain=True)
            return [ret]
        else:
            return valid_cards[:min_num_gain]

    def topdeck_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_topdeck: int = 0,
        max_num_topdeck: int = -1,
    ) -> List["Card"]:
        if card.name == "Artisan":
            ret = self.artisan(player=player, game=game, valid_cards=valid_cards, topdeck=True)
            return [ret]
        elif card.name == "Harbinger":
            ret = self.harbinger(player=player, valid_cards=valid_cards)
            return [] if ret is None else [ret]
        elif card.name == "Bureaucrat":
            ret = self.bureaucrat(player=player, valid_cards=valid_cards)
            return [ret]
        else:
            return valid_cards[:min_num_topdeck]

    def multi_play_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        required: bool = True,
    ) -> Optional["Card"]:
        if card.name == "Throne Room":
            return self.throne_room(player=player, valid_cards=valid_cards)
        else:
            if required:
                return valid_cards[0]
            else:
                return None

    # CARD SPECIFIC IMPLEMENTATIONS

    def moneylender(self, player: "Player") -> bool:
        return True

    def vassal(self, player: "Player", relevant_cards: Optional[List[Card]]) -> bool:
        return True

    def sentry(
        self,
        player: "Player",
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
                valid_cards=valid_cards, player=player, game=game
            )
        if discard:
            if not valid_cards:
                return []
            return [
                card
                for card in valid_cards
                if card.name == "Copper"
                or CardType.Victory in card.type
                or CardType.Curse in card.type
            ]
        if binary:
            return False

        raise InvalidBotImplementation(
            "Either gain, topdeck or binary must be true when playing sentry"
        )

    def library(self, player: "Player", relevant_cards: Optional[List[Card]]) -> bool:
        if player.state.actions == 0:
            return True
        else:
            return False

    def cellar(self, player: "Player", valid_cards: List[Card]) -> List[Card]:
        return [
            card
            for card in valid_cards
            if card.name == "Copper" or CardType.Victory in card.type or CardType.Curse in card.type
        ]

    def poacher(
        self, player: "Player", valid_cards: List[Card], num_discard: Optional[int]
    ) -> List[Card]:
        if not num_discard:
            return []
        discard_order = self.sort_for_discard(
            cards=valid_cards, actions=player.state.actions
        )
        return discard_order[:num_discard]

    def militia(
        self, player: "Player", valid_cards: List[Card], num_discard: Optional[int]
    ) -> List[Card]:
        if not num_discard:
            return []
        discard_order = self.sort_for_discard(
            cards=valid_cards, actions=player.state.actions
        )
        return discard_order[:num_discard]

    def remodel(
        self, player: "Player", valid_cards: List[Card], trash: bool = False, gain: bool = False
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
        self, player: "Player", valid_cards: List[Card], trash: bool = False, gain: bool = False
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

    def chapel(self, player: "Player", game: "Game", valid_cards: List[Card]) -> List[Card]:
        trash_cards = self.determine_trash_cards(
            valid_cards=valid_cards, player=player, game=game
        )
        while len(trash_cards) > 4:
            trash_cards.pop()
        return trash_cards

    def artisan(
        self,
        player: "Player",
        game: "Game",
        valid_cards: Optional[List[Card]] = None,
        gain: bool = False,
        topdeck: bool = False,
    ) -> Card:
        if topdeck:
            for card in player.hand.cards:
                if CardType.Action in card.type and player.state.actions == 0:
                    return card
            else:
                return player.hand.cards[-1]
        if gain:
            if game.supply.pile_length(pile_name="Province") < 5:
                return duchy
            else:
                return silver

        raise InvalidBotImplementation(
            "Either gain or topdeck must be true when playing artisan"
        )

    def workshop(
        self,
        player: "Player",
        game: "Game",
    ) -> Card:
        if game.supply.pile_length(pile_name="Province") < 3:
            return estate
        else:
            return silver

    def harbinger(
        self,
        player: "Player",
        valid_cards: List[Card],
    ) -> Optional[Card]:
        # Do not topdeck victory cards
        best_topdeck = [card for card in valid_cards if CardType.Victory not in card.type]
        if not best_topdeck:
            return None
        # Topdeck highest price card if price > 2
        max_price_card = max(best_topdeck, key=lambda card: card.cost)
        if max_price_card.cost > 2:
            return max_price_card
        else:
            return None

    def bureaucrat(
        self,
        player: "Player",
        valid_cards: List[Card],
    ) -> Card:
        sorted_cards = sorted(valid_cards, key=lambda card: card.cost)
        return sorted_cards[0]

    def throne_room(self, player: "Player", valid_cards: List[Card]) -> Card:
        # Double play most expensive card
        max_price_card = max(valid_cards, key=lambda card: card.cost)
        return max_price_card


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
        super().__init__(decider=OptimizedBotDecider(), player_id=player_id)

    def is_attacked(self, player: "Player", attack_card: Card, game: "Game") -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                return False
        return True
