from typing import TYPE_CHECKING, Iterable, Literal, cast, overload

from pyminion.bots.bot import Bot, BotDecider
from pyminion.core import Action, CardType, Card, DeckCounter, Treasure, Victory, get_action_cards, get_treasure_cards, get_victory_cards, get_score_cards
from pyminion.decider import Decider
from pyminion.exceptions import InvalidBotImplementation
from pyminion.expansions.base import duchy, estate, curse, gold, silver, copper
from pyminion.expansions.intrigue import Baron, Courtier, Lurker, Minion, Nobles, Pawn, Steward, Torturer
from pyminion.expansions.seaside import NativeVillage
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


class OptimizedBotDecider(BotDecider):
    """
    Implements opinionated logic for playing and reacting to all cards in the base set.

    The intention is to inherit from this class to make concrete bot implementations.
    If inheriting from this bot, it is possible to change the way that a single card is executed
    by overwriting the card specific method at the bottom of this file.

    """

    @staticmethod
    def get_best_victory_card(valid_cards: list[Card], player: Player) -> Victory|None:
        """
        Get the victory card that has the highest score.

        """

        best_victory = max(
            get_victory_cards(valid_cards),
            key=lambda card: card.score(player),
            default=None,
        )
        return best_victory

    @staticmethod
    def sort_for_discard(cards: list[Card], actions: int, player: Player, game: "Game") -> list[Card]:
        """
        Sort list of cards from best discard candidate to worst discard candidate.
        First sort cards from lowest cost to highest cost. Then rearrange depending on remaining actions.
        If player has no remaining actions, prioritize discarding victory then action, then treasures.
        If player has remaining actions, prioritize discarding victory then treasure and action equally.

        """

        sorted_cards = sorted(cards, key=lambda card: card.get_cost(player, game))
        score_cards = list(get_score_cards(sorted_cards))
        non_score_cards = [
            card
            for card in sorted_cards
            if CardType.Victory not in card.type and CardType.Curse not in card.type
        ]
        treasure_cards = [card for card in non_score_cards if CardType.Treasure in card.type]
        action_cards = [
            card for card in non_score_cards if CardType.Treasure not in card.type
        ]
        if actions == 0:
            return score_cards + action_cards + treasure_cards
        else:
            return score_cards + non_score_cards

    @staticmethod
    def determine_set_aside_cards(cards: Iterable[Card], player: Player, game: "Game") -> list[Card]:
        num_terminal = sum(1 for c in get_action_cards(cards) if c.actions == 0)

        prioritized_cards: list[tuple[int, Card]] = []
        for card in cards:
            cost = card.get_cost(player, game)
            # set aside terminal action cards if we don't have enough actions to play them
            if num_terminal > player.state.actions and CardType.Action in card.type and cast(Action, card).actions == 0:
                priority = 100 + cost.money + 2 * cost.potions
            else:
                priority = 200 + cost.money + 2 * cost.potions

            prioritized_cards.append((priority, card))

        prioritized_cards.sort(key=lambda x: x[0])
        set_aside_cards = [x[1] for x in prioritized_cards]
        return set_aside_cards

    @staticmethod
    def get_optional_discard(cards: list[Card], player: Player) -> list[Card]:
        discard_cards: list[Card] = []
        actions = player.state.actions
        for card in cards:
            if CardType.Treasure in card.type:
                continue
            elif CardType.Curse in card.type:
                discard_cards.append(card)
            elif CardType.Victory in card.type and CardType.Action not in card.type:
                discard_cards.append(card)
            elif actions == 0 and CardType.Action in card.type:
                discard_cards.append(card)

        return discard_cards

    @staticmethod
    def determine_trash_cards(
        valid_cards: list[Card], player: Player, game: "Game", required: bool = False
    ) -> list[Card]:
        """
        Determine which cards should be trashed:

        Always trash Curse
        Trash Estate if number of provinces in supply >= 5
        Trash Copper if money in deck > 3 (keep enough to buy silver)
        If trashing is required, sort cards by increasing cost

        """

        num_provinces = game.supply.pile_length("Province")
        deck_money = player.get_deck_money()

        prioritized_cards: list[tuple[int, Card]] = []
        for card in valid_cards:
            if CardType.Curse in card.type:
                priority = 1
            elif card.name == "Estate" and num_provinces >= 5:
                priority = 2
            elif card.name == "Copper" and deck_money > 3:
                priority = 3
                deck_money -= 1
            elif required:
                cost = card.get_cost(player, game)
                priority = 100 + cost.money + 2 * cost.potions
            else:
                priority = 0

            if priority > 0:
                prioritized_cards.append((priority, card))

        prioritized_cards.sort(key=lambda x: x[0])
        trash_cards = [x[1] for x in prioritized_cards]
        return trash_cards

    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: list[Card]|None = None,
    ) -> bool:
        if card.name == "Moneylender":
            return self.moneylender(player=player, game=game)
        elif card.name == "Vassal":
            return self.vassal(player=player, game=game, relevant_cards=relevant_cards)
        elif card.name == "Sentry":
            return self.sentry(player=player, game=game, relevant_cards=relevant_cards, binary=True)
        elif card.name == "Library":
            return self.library(player=player, game=game, relevant_cards=relevant_cards)
        elif card.name == "Moat":
            return self.moat(player=player, game=game, relevant_cards=relevant_cards)
        elif card.name == "Diplomat":
            return self.diplomat(player, game, binary=True)
        elif card.name == "Masquerade":
            return self.masquerade(player, game, binary=True)
        elif card.name == "Mill":
            return self.mill(player, game, binary=True)
        elif card.name == "Mining Village":
            return self.mining_village(player, game)
        elif card.name == "Pirate":
            return self.pirate_binary(player, game)
        elif card.name == "Sailor":
            return self.sailor_binary(prompt, player, game, relevant_cards)
        elif card.name == "Treasury":
            return self.treasury(prompt, player, game, relevant_cards)
        elif card.name == "Alchemist":
            return self.alchemist(player, game)
        elif card.name == "Herbalist":
            assert relevant_cards is not None
            return self.herbalist(player, game, relevant_cards[0])
        elif card.name == "Scrying Pool":
            assert relevant_cards is not None
            return self.scrying_pool(prompt, player, game, relevant_cards)
        elif card.name == "University":
            return self.university_binary(player, game, relevant_cards)
        else:
            return super().binary_decision(prompt, card, player, game, relevant_cards)

    def multiple_option_decision(
        self,
        card: "Card",
        options: list[str],
        player: "Player",
        game: "Game",
        num_choices: int = 1,
        unique: bool = True,
    ) -> list[int]:
        if card.name == "Baron":
            ret = self.baron(player, game)
            return [ret]
        elif card.name == "Courtier":
            return self.courtier(player, game, num_choices=num_choices, options=True)
        elif card.name == "Lurker":
            ret = self.lurker(player, game, options=True)
            return [ret]
        elif card.name == "Minion":
            ret = self.minion(player, game)
            return [ret]
        elif card.name == "Native Village":
            ret = self.native_village(player, game)
            return [ret]
        elif card.name == "Nobles":
            ret = self.nobles(player, game)
            return [ret]
        elif card.name == "Pawn":
            return self.pawn(player, game)
        elif card.name == "Steward":
            ret = self.steward(player, game, options=True)
            return [ret]
        elif card.name == "Torturer":
            ret = self.torturer(player, game, options=True)
            return [ret]
        elif card.name == "Golem":
            ret = self.golem(player, game)
            return [ret]
        else:
            return super().multiple_option_decision(card, options, player, game, num_choices, unique)

    def discard_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_discard: int = 0,
        max_num_discard: int = -1,
    ) -> list["Card"]:
        if card.name == "Cellar":
            return self.cellar(player=player, game=game, valid_cards=valid_cards)
        elif card.name == "Poacher":
            return self.poacher(player=player, game=game, valid_cards=valid_cards, num_discard=min_num_discard)
        elif card.name == "Militia":
            return self.militia(player=player, game=game, valid_cards=valid_cards, num_discard=min_num_discard)
        elif card.name == "Sentry":
            return self.sentry(player=player, game=game, valid_cards=valid_cards, discard=True)
        elif card.name == "Diplomat":
            return self.diplomat(player, game, valid_cards, min_num_discard, discard=True)
        elif card.name == "Mill":
            return self.mill(player, game, discard=True)
        elif card.name == "Torturer":
            return self.torturer(player, game, valid_cards=valid_cards, num_discard=min_num_discard, discard=True)
        elif card.name == "Lookout":
            ret = self.lookout(player, game, valid_cards, discard=True)
            return [ret]
        elif card.name == "Sea Witch":
            return self.sea_witch(player, game, valid_cards=valid_cards, num_discard=min_num_discard)
        elif card.name == "Tide Pools":
            return self.tide_pools(player, game, valid_cards=valid_cards, num_discard=min_num_discard)
        elif card.name == "Warehouse":
            return self.warehouse(player, game, valid_cards=valid_cards, num_discard=min_num_discard)
        else:
            return super().discard_decision(prompt, card, valid_cards, player, game, min_num_discard, max_num_discard)

    def trash_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_trash: int = 0,
        max_num_trash: int = -1,
    ) -> list["Card"]:
        if card.name == "Remodel":
            ret = self.remodel(player=player, game=game, valid_cards=valid_cards, trash=True)
            return [ret]
        elif card.name == "Mine":
            ret = self.mine(player=player, game=game, valid_cards=valid_cards, trash=True)
            return [ret]
        elif card.name == "Chapel":
            return self.chapel(player=player, game=game, valid_cards=valid_cards)
        elif card.name == "Sentry":
            return self.sentry(player=player, game=game, valid_cards=valid_cards, trash=True)
        elif card.name == "Bandit":
            ret = self.bandit(player, game, valid_cards)
            return [ret]
        elif card.name == "Lurker":
            ret = self.lurker(player, game, valid_cards, trash=True)
            return [ret]
        elif card.name == "Masquerade":
            ret = self.masquerade(player, game, valid_cards, trash=True)
            return [ret]
        elif card.name == "Replace":
            ret = self.replace(player, game, valid_cards, trash=True)
            return [ret]
        elif card.name == "Steward":
            return self.steward(player, game, valid_cards=valid_cards, trash=True)
        elif card.name == "Trading Post":
            return self.trading_post(player, game, valid_cards)
        elif card.name == "Upgrade":
            ret = self.upgrade(player, game, valid_cards, trash=True)
            return [ret]
        elif card.name == "Lookout":
            ret = self.lookout(player, game, valid_cards, trash=True)
            return [ret]
        elif card.name == "Sailor":
            ret = self.sailor_trash(player, game, valid_cards)
            return [ret]
        elif card.name == "Salvager":
            ret = self.salvager(player, game, valid_cards)
            return [ret]
        elif card.name == "Apprentice":
            ret = self.apprentice(player, game, valid_cards)
            return [ret]
        elif card.name == "Transmute":
            ret = self.transmute(player, game, valid_cards)
            return [ret]
        else:
            return super().trash_decision(prompt, card, valid_cards, player, game, min_num_trash, max_num_trash)

    def gain_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_gain: int = 0,
        max_num_gain: int = -1,
    ) -> list["Card"]:
        if card.name == "Artisan":
            ret = self.artisan(player=player, game=game, gain=True)
            return [ret]
        elif card.name == "Workshop":
            ret = self.workshop(player=player, game=game)
            return [ret]
        elif card.name == "Remodel":
            ret = self.remodel(player=player, game=game, valid_cards=valid_cards, gain=True)
            return [ret]
        elif card.name == "Mine":
            ret = self.mine(player=player, game=game, valid_cards=valid_cards, gain=True)
            return [ret]
        elif card.name == "Ironworks":
            ret = self.ironworks(player, game, valid_cards)
            return [ret]
        elif card.name == "Lurker":
            ret = self.lurker(player, game, valid_cards, gain=True)
            return [ret]
        elif card.name == "Replace":
            ret = self.replace(player, game, valid_cards, gain=True)
            return [ret]
        elif card.name == "Swindler":
            ret = self.swindler(player, game, valid_cards)
            return [ret]
        elif card.name == "Upgrade":
            ret = self.upgrade(player, game, valid_cards, gain=True)
            return [ret]
        elif card.name == "Blockade":
            ret = self.blockade(player, game, valid_cards)
            return [ret]
        elif card.name == "Pirate":
            ret = self.pirate_gain(player, game, valid_cards)
            return [ret]
        elif card.name == "Smugglers":
            ret = self.smugglers(player, game, valid_cards)
            return [ret]
        elif card.name == "University":
            ret = self.university_gain(player, game, valid_cards)
            return [ret]
        else:
            return super().gain_decision(prompt, card, valid_cards, player, game, min_num_gain, max_num_gain)

    def topdeck_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_topdeck: int = 0,
        max_num_topdeck: int = -1,
    ) -> list["Card"]:
        if card.name == "Artisan":
            ret = self.artisan(player=player, game=game, valid_cards=valid_cards, topdeck=True)
            return [ret]
        elif card.name == "Harbinger":
            ret = self.harbinger(player=player, game=game, valid_cards=valid_cards)
            return [] if ret is None else [ret]
        elif card.name == "Bureaucrat":
            ret = self.bureaucrat(player=player, game=game, valid_cards=valid_cards)
            return [ret]
        elif card.name == "Courtyard":
            ret = self.courtyard(player, game, valid_cards)
            return [ret]
        elif card.name == "Patrol":
            return self.patrol(player, game, valid_cards)
        elif card.name == "Secret Passage":
            ret = self.secret_passage(player, game, valid_cards=valid_cards, topdeck=True)
            return [ret]
        elif card.name == "Apothecary":
            return self.apothecary(player, game, valid_cards)
        else:
            return super().topdeck_decision(prompt, card, valid_cards, player, game, min_num_topdeck, max_num_topdeck)

    def deck_position_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        num_deck_cards: int,
    ) -> int:
        if card.name == "Secret Passage":
            return self.secret_passage(player, game, num_deck_cards=num_deck_cards, pos=True)
        else:
            return super().deck_position_decision(prompt, card, player, game, num_deck_cards)

    def reveal_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_reveal: int = 0,
        max_num_reveal: int = -1,
    ) -> list["Card"]:
        if card.name == "Courtier":
            ret = self.courtier(player, game, valid_cards=valid_cards, reveal=True)
            return [ret]
        else:
            return super().reveal_decision(prompt, card, valid_cards, player, game, min_num_reveal, max_num_reveal)

    def pass_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_pass: int = 0,
        max_num_pass: int = -1,
    ) -> list["Card"]:
        if card.name == "Masquerade":
            ret = self.masquerade(player, game, valid_cards, pass_=True)
            return [ret]
        else:
            return super().pass_decision(prompt, card, valid_cards, player, game, min_num_pass, max_num_pass)

    def name_card_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_name: int = 0,
        max_num_name: int = -1,
    ) -> list["Card"]:
        if card.name == "Wishing Well":
            ret = self.wishing_well(player, game)
            return [ret]
        else:
            return super().name_card_decision(prompt, card, valid_cards, player, game, min_num_name, max_num_name)

    def multi_play_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        required: bool = True,
    ) -> Card|None:
        if card.name == "Throne Room":
            return self.throne_room(player=player, game=game, valid_cards=valid_cards)
        else:
            return super().multi_play_decision(prompt, card, valid_cards, player, game, required)

    def set_aside_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: list["Card"],
        player: "Player",
        game: "Game",
        min_num_set_aside: int = 0,
        max_num_set_aside: int = -1,
    ) -> list["Card"]:
        if card.name == "Haven":
            ret = self.haven(player, game, valid_cards)
            return [ret]
        elif card.name == "Island":
            ret = self.island(player, game, valid_cards)
            return [ret]
        else:
            return super().set_aside_decision(prompt, card, valid_cards, player, game, min_num_set_aside, max_num_set_aside)

    # CARD SPECIFIC IMPLEMENTATIONS

    def moneylender(self, player: "Player", game: "Game") -> bool:
        return True

    def vassal(self, player: "Player", game: "Game", relevant_cards: list[Card]|None) -> bool:
        return True

    @overload
    def sentry(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        relevant_cards: list[Card]|None = None,
        trash: Literal[True] = True,
        discard: Literal[False] = False,
        binary: Literal[False] = False,
    ) -> list[Card]:
        ...

    @overload
    def sentry(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        relevant_cards: list[Card]|None = None,
        trash: Literal[False] = False,
        discard: Literal[True] = True,
        binary: Literal[False] = False,
    ) -> list[Card]:
        ...

    @overload
    def sentry(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        relevant_cards: list[Card]|None = None,
        trash: Literal[False] = False,
        discard: Literal[False] = False,
        binary: Literal[True] = True,
    ) -> bool:
        ...

    def sentry(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        relevant_cards: list[Card]|None = None,
        trash: bool = False,
        discard: bool = False,
        binary: bool = False,
    ) -> list[Card]|bool:
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

    def library(self, player: "Player", game: "Game", relevant_cards: list[Card]|None) -> bool:
        if player.state.actions == 0:
            return True
        else:
            return False

    def cellar(self, player: "Player", game: "Game", valid_cards: list[Card]) -> list[Card]:
        return [
            card
            for card in valid_cards
            if card.name == "Copper" or CardType.Victory in card.type or CardType.Curse in card.type
        ]

    def moat(self, player: "Player", game: "Game", relevant_cards: list[Card]|None) -> bool:
        return True

    def poacher(
        self, player: "Player", game: "Game", valid_cards: list[Card], num_discard: int|None
    ) -> list[Card]:
        if not num_discard:
            return []
        discard_order = self.sort_for_discard(
            cards=valid_cards, actions=player.state.actions, player=player, game=game
        )
        return discard_order[:num_discard]

    def militia(
        self, player: "Player", game: "Game", valid_cards: list[Card], num_discard: int|None
    ) -> list[Card]:
        if not num_discard:
            return []
        discard_order = self.sort_for_discard(
            cards=valid_cards, actions=player.state.actions, player=player, game=game
        )
        return discard_order[:num_discard]

    def remodel(
        self, player: "Player", game: "Game", valid_cards: list[Card], trash: bool = False, gain: bool = False
    ) -> Card:
        if trash:
            min_price_card = min(valid_cards, key=lambda card: card.get_cost(player, game))
            return min_price_card

        if gain:
            max_price_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
            return max_price_card

        raise InvalidBotImplementation(
            "Either gain or trash must be true when playing remodel"
        )

    def mine(
        self, player: "Player", game: "Game", valid_cards: list[Card], trash: bool = False, gain: bool = False
    ) -> Card:
        if trash:
            min_price_card = min(valid_cards, key=lambda card: card.get_cost(player, game))
            return min_price_card

        if gain:
            max_price_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
            return max_price_card

        raise InvalidBotImplementation(
            "Either gain or trash must be true when playing mine"
        )

    def chapel(self, player: "Player", game: "Game", valid_cards: list[Card]) -> list[Card]:
        trash_cards = self.determine_trash_cards(
            valid_cards=valid_cards, player=player, game=game
        )
        trash_cards = trash_cards[:4]
        return trash_cards

    def artisan(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
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
            if game.supply.pile_length("Province") < 5 and game.supply.pile_length("Duchy") > 0:
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
        if game.supply.pile_length("Province") < 3 and game.supply.pile_length("Estate") > 0:
            return estate
        else:
            return silver

    def harbinger(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card|None:
        # Do not topdeck victory cards
        best_topdeck = [card for card in valid_cards if CardType.Victory not in card.type]
        if not best_topdeck:
            return None
        # Topdeck highest price card if price > 2
        max_price_card = max(best_topdeck, key=lambda card: card.get_cost(player, game))
        if max_price_card.get_cost(player, game) > 2:
            return max_price_card
        else:
            return None

    def bureaucrat(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        sorted_cards = sorted(valid_cards, key=lambda card: card.get_cost(player, game))
        return sorted_cards[0]

    def throne_room(self, player: "Player", game: "Game", valid_cards: list[Card]) -> Card:
        # Double play most expensive card
        max_price_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
        return max_price_card

    def bandit(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        min_price_card = min(valid_cards, key=lambda card: card.get_cost(player, game))
        return min_price_card

    def baron(
        self,
        player: "Player",
        game: "Game",
    ) -> int:
        return Baron.Choice.DiscardEstate

    @overload
    def courtier(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_choices: int = 0,
        reveal: Literal[True] = True,
        options: Literal[False] = False,
    ) -> Card:
        ...

    @overload
    def courtier(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_choices: int = 0,
        reveal: Literal[False] = False,
        options: Literal[True] = True,
    ) -> list[int]:
        ...

    def courtier(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_choices: int = 0,
        reveal: bool = False,
        options: bool = False,
    ) -> Card|list[int]:
        if reveal:
            assert valid_cards is not None
            # find the card with the most types
            num_types = 0
            reveal_card = valid_cards[0]
            for c in valid_cards:
                if len(c.type) > num_types:
                    num_types = len(c.type)
                    reveal_card = c
            return reveal_card
        elif options:
            assert num_choices > 0
            counter = DeckCounter(player.get_all_cards())
            gold_count = counter[gold]
            has_actions = any(CardType.Action in c.type for c in player.hand.cards)

            # prioritize choices
            choices: list[int] = []
            if has_actions:
                choices.append(Courtier.Choice.Action)
            if gold_count < 4:
                choices.append(Courtier.Choice.GainGold)
            choices.append(Courtier.Choice.Money)

            # add remaining choices
            for c in Courtier.Choice:
                if c.value not in choices:
                    choices.append(c.value)

            choices = choices[:num_choices]
            return choices
        else:
            raise InvalidBotImplementation(
                "Either reveal or options must be true when playing courier"
            )

    def courtyard(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        if player.state.actions == 0:
            for card in valid_cards:
                if CardType.Action in card.type:
                    return card

        return valid_cards[-1]

    @overload
    def diplomat(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_discard: int = 0,
        binary: Literal[True] = True,
        discard: Literal[False] = False,
    ) -> bool:
        ...

    @overload
    def diplomat(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_discard: int = 0,
        binary: Literal[False] = False,
        discard: Literal[True] = True,
    ) -> list[Card]:
        ...

    def diplomat(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_discard: int = 0,
        binary: bool = False,
        discard: bool = False,
    ) -> bool|list[Card]:
        if binary:
            return True
        elif discard:
            assert valid_cards is not None
            discard_order = self.sort_for_discard(
                cards=valid_cards, actions=player.state.actions, player=player, game=game
            )
            return discard_order[:num_discard]
        else:
            raise InvalidBotImplementation(
                "Either binary or discard must be true when playing diplomat"
            )

    def ironworks(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        best_victory = self.get_best_victory_card(valid_cards, player)
        if game.supply.pile_length(pile_name="Province") < 3 and best_victory is not None:
            return best_victory
        else:
            return silver

    @overload
    def lurker(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: Literal[True] = True,
        trash: Literal[False] = False,
        gain: Literal[False] = False,
    ) -> int:
        ...

    @overload
    def lurker(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: Literal[False] = False,
        trash: Literal[True] = True,
        gain: Literal[False] = False,
    ) -> Card:
        ...

    @overload
    def lurker(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: Literal[False] = False,
        trash: Literal[False] = False,
        gain: Literal[True] = True,
    ) -> Card:
        ...

    def lurker(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: bool = False,
        trash: bool = False,
        gain: bool = False,
    ) -> int|Card:
        if options:
            if any(CardType.Action in c.type for c in game.trash.cards):
                return Lurker.Choice.GainAction
            else:
                return Lurker.Choice.TrashAction
        elif trash or gain:
            assert valid_cards is not None
            max_price_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
            return max_price_card
        else:
            raise InvalidBotImplementation(
                "Either options, trash, or gain must be true when playing lurker"
            )

    @overload
    def masquerade(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        pass_: Literal[True] = True,
        binary: Literal[False] = False,
        trash: Literal[False] = False,
    ) -> Card:
        ...

    @overload
    def masquerade(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        pass_: Literal[False] = False,
        binary: Literal[True] = True,
        trash: Literal[False] = False,
    ) -> bool:
        ...

    @overload
    def masquerade(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        pass_: Literal[False] = False,
        binary: Literal[False] = False,
        trash: Literal[True] = True,
    ) -> Card:
        ...

    def masquerade(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        pass_: bool = False,
        binary: bool = False,
        trash: bool = False,
    ) -> bool|Card:
        if pass_:
            assert valid_cards is not None
            cards = self.determine_trash_cards(valid_cards, player, game, required=True)
            return cards[0]
        elif binary:
            cards = self.determine_trash_cards(player.hand.cards, player, game)
            return len(cards) > 0
        elif trash:
            assert valid_cards is not None
            cards = self.determine_trash_cards(valid_cards, player, game)
            return cards[0]
        else:
            raise InvalidBotImplementation(
                "Either pass_, binary, or trash must be true when playing masquerade"
            )

    @overload
    def mill(
        self,
        player: "Player",
        game: "Game",
        binary: Literal[True] = True,
        discard: Literal[False] = False,
    ) -> bool:
        ...

    @overload
    def mill(
        self,
        player: "Player",
        game: "Game",
        binary: Literal[False] = False,
        discard: Literal[True] = True,
    ) -> list[Card]:
        ...

    def mill(
        self,
        player: "Player",
        game: "Game",
        binary: bool = False,
        discard: bool = False,
    ) -> bool|list[Card]:
        actions = player.state.actions
        cards = self.sort_for_discard(player.hand.cards, actions, player, game)
        cards = cards[:2]
        if binary:
            if len(cards) < 2:
                return False
            money = 0
            for card in get_treasure_cards(cards):
                money += card.money
            # discard cards if they provide less money than the
            # +$2 mill will give for discarding
            return money < 2
        elif discard:
            return cards
        else:
            raise InvalidBotImplementation(
                "Either binary or discard must be true when playing mill"
            )

    def mining_village(
        self,
        player: "Player",
        game: "Game",
    ) -> bool:
        return game.supply.pile_length("Province") < 3

    def minion(
        self,
        player: "Player",
        game: "Game",
    ) -> int:
        has_action_cards = False
        hand_money = 0
        for card in player.hand.cards:
            if CardType.Action in card.type:
                has_action_cards = True
            if CardType.Treasure in card.type:
                assert isinstance(card, Treasure)
                hand_money += card.money

        # don't discard hand if we can play more actions or if we have money in hand
        if (has_action_cards and player.state.actions > 0) or hand_money >= 3:
            return Minion.Choice.Money
        return Minion.Choice.DiscardDrawAttack

    def nobles(
        self,
        player: "Player",
        game: "Game",
    ) -> int:
        action_card_count = sum(1 for _ in get_action_cards(player.hand.cards))
        if action_card_count > player.state.actions:
            return Nobles.Choice.Actions
        return Nobles.Choice.Cards

    def patrol(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> list[Card]:
        cards = sorted(
            valid_cards,
            key=lambda card: card.get_cost(player, game),
        )
        return cards

    def pawn(
        self,
        player: "Player",
        game: "Game",
    ) -> list[int]:
        action_card_count = 0
        total_money = player.state.money
        for card in player.hand.cards:
            if CardType.Action in card.type:
                action_card_count += 1
            if CardType.Treasure in card.type:
                assert isinstance(card, Treasure)
                total_money += card.money

        choices: list[int] = []
        if action_card_count > player.state.actions:
            choices.append(Pawn.Choice.Action)

        if total_money < 2:
            choices.append(Pawn.Choice.Money)
        elif total_money > 8:
            choices.append(Pawn.Choice.Buy)

        if len(choices) < 2:
            choices.append(Pawn.Choice.Card)
        if len(choices) < 2:
            choices.append(Pawn.Choice.Money)

        return choices

    def replace(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
        trash: bool = False,
        gain: bool = False,
    ) -> Card:
        num_provinces = game.supply.pile_length("Province")
        if trash:
            has_gold = False
            has_curse = False
            for card in valid_cards:
                if CardType.Curse in card.type:
                    has_curse = True
                elif card.name == "Gold":
                    has_gold = True

            if has_gold and num_provinces < 5:
                return gold

            if has_curse:
                return curse

            min_price_card = min(valid_cards, key=lambda card: card.get_cost(player, game))
            return min_price_card

        if gain:
            victory_cards = list(get_victory_cards(valid_cards))
            victory_cards.sort(key=lambda c: c.score(player), reverse=True)
            if len(victory_cards) > 0:
                victory_card = victory_cards[0]
                score = victory_card.score(player)
                if score >= 6:
                    return victory_card
                elif score >= 3 and num_provinces < 5:
                    return victory_card
                elif num_provinces < 3:
                    return victory_card

            max_price_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
            return max_price_card

        raise InvalidBotImplementation(
            "Either trash or gain must be true when playing replace"
        )

    @overload
    def secret_passage(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_deck_cards: int = -1,
        topdeck: Literal[True] = True,
        pos: Literal[False] = False,
    ) -> Card:
        ...

    @overload
    def secret_passage(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_deck_cards: int = -1,
        topdeck: Literal[False] = False,
        pos: Literal[True] = True,
    ) -> int:
        ...

    def secret_passage(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_deck_cards: int = -1,
        topdeck: bool = False,
        pos: bool = False,
    ) -> Card|int:
        if topdeck:
            assert valid_cards is not None
            return valid_cards[-1]

        if pos:
            assert num_deck_cards >= 0
            return num_deck_cards # put the card on top of the deck

        raise InvalidBotImplementation(
            "Either topdeck or pos must be true when playing secret passage"
        )

    @overload
    def steward(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: Literal[True] = True,
        trash: Literal[False] = False,
    ) -> int:
        ...

    @overload
    def steward(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: Literal[False] = False,
        trash: Literal[True] = True,
    ) -> list[Card]:
        ...

    def steward(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        options: bool = False,
        trash: bool = False,
    ) -> int|list[Card]:
        if options:
            trash_cards = self.determine_trash_cards(player.hand.cards, player, game, required=False)
            if player.state.actions > 0:
                return Steward.Choice.Cards
            elif len(trash_cards) >= 2:
                return Steward.Choice.Trash
            else:
                return Steward.Choice.Money

        if trash:
            assert valid_cards is not None
            trash_cards = self.determine_trash_cards(valid_cards, player, game, required=True)
            return trash_cards[:2]

        raise InvalidBotImplementation(
            "Either options or trash must be true when playing steward"
        )

    def swindler(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        # prioritize cards
        prioritized_cards: list[tuple[int, Card]] = []
        for card in valid_cards:
            if card.name == "Curse":
                # prioritize giving opponents curses first
                prioritized_cards.append((1, card))
            elif CardType.Attack in card.type:
                # lower priority for giving opponents attack cards
                prioritized_cards.append((3, card))
            elif CardType.Victory in card.type:
                # lower priority for giving opponents victory cards
                prioritized_cards.append((4, card))
            else:
                # prioritize giving all other cards second
                prioritized_cards.append((2, card))
        prioritized_cards.sort(key=lambda x: x[0])

        return prioritized_cards[0][1]

    @overload
    def torturer(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_discard: int = -1,
        options: Literal[True] = True,
        discard: Literal[False] = False,
    ) -> int:
        ...

    @overload
    def torturer(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_discard: int = -1,
        options: Literal[False] = False,
        discard: Literal[True] = True,
    ) -> list[Card]:
        ...

    def torturer(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None = None,
        num_discard: int = -1,
        options: bool = False,
        discard: bool = False,
    ) -> int|list[Card]:
        if options:
            if game.supply.pile_length("Curse") == 0:
                return Torturer.Choice.GainCurse

            discard_cards = self.get_optional_discard(player.hand.cards, player)
            max_discard = min(2, len(player.hand))
            if len(discard_cards) >= max_discard:
                return Torturer.Choice.Discard

            return Torturer.Choice.GainCurse

        if discard:
            assert valid_cards is not None
            assert num_discard >= 0
            discard_cards = self.sort_for_discard(
                valid_cards,
                player.state.actions,
                player,
                game,
            )
            return discard_cards[:num_discard]

        raise InvalidBotImplementation(
            "Either options or discard must be true when playing torturer"
        )

    def trading_post(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> list[Card]:
        trash_cards = self.determine_trash_cards(valid_cards, player, game, required=True)
        return trash_cards[:2]

    def upgrade(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
        trash: bool = False,
        gain: bool = False,
    ) -> Card:
        if trash:
            min_price_card = min(valid_cards, key=lambda card: card.get_cost(player, game))
            return min_price_card

        if gain:
            max_price_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
            return max_price_card

        raise InvalidBotImplementation(
            "Either trash or gain must be true when playing upgrade"
        )

    def wishing_well(
        self,
        player: "Player",
        game: "Game",
    ) -> Card:
        return copper

    def blockade(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        best_victory = self.get_best_victory_card(valid_cards, player)
        if game.supply.pile_length(pile_name="Province") < 3 and best_victory is not None:
            return best_victory
        return silver

    def haven(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        cards = self.determine_set_aside_cards(valid_cards, player, game)
        return cards[0]

    def island(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        deck_money = player.get_deck_money()

        prioritized_cards: list[tuple[int, Card]] = []
        for card in valid_cards:
            if len(card.type) == 1 and card.type[0] == CardType.Victory:
                priority = 1
            elif card.name == "Copper" and deck_money > 3:
                priority = 2
            elif card.name == "Curse":
                priority = 3
            else:
                priority = 100 + card.get_cost(player, game).money

            prioritized_cards.append((priority, card))

        result = min(prioritized_cards, key=lambda x: x[0])
        return result[1]

    def lookout(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
        trash: bool = False,
        discard: bool = False,
    ) -> Card:
        if trash:
            cards = self.determine_trash_cards(valid_cards, player, game, required=True)
            return cards[0]

        if discard:
            cards = self.sort_for_discard(valid_cards, player.state.actions, player, game)
            return cards[0]

        raise InvalidBotImplementation(
            "Either trash or discard must be true when playing lookout"
        )

    def native_village(
        self,
        player: "Player",
        game: "Game",
    ) -> int:
        mat_count = len(player.get_mat("Native Village"))
        if mat_count == 0:
            return NativeVillage.Choice.AddToMat

        native_village_card_count = sum(1 for c in player.hand.cards if c.name == "Native Village")
        if native_village_card_count > 0:
            return NativeVillage.Choice.AddToMat

        return NativeVillage.Choice.GetFromMat

    def pirate_binary(
        self,
        player: Player,
        game: "Game",
    ) -> bool:
        return True

    def pirate_gain(
        self,
        player: Player,
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        most_expensive_card = max(valid_cards, key=lambda card: card.get_cost(player, game))
        return most_expensive_card

    def sailor_binary(
        self,
        prompt: str,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None,
    ) -> bool:
        if "trash" in prompt:
            assert valid_cards is not None
            trash_cards = self.determine_trash_cards(valid_cards, player, game, required=False)
            return len(trash_cards) > 0
        elif "play" in prompt:
            return True

        raise InvalidBotImplementation("Unknown prompt for sailor")

    def sailor_trash(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        trash_cards = self.determine_trash_cards(valid_cards, player, game, required=False)
        return trash_cards[0]

    def salvager(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        trash_cards = self.determine_trash_cards(valid_cards, player, game, required=True)
        return trash_cards[0]

    def sea_witch(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
        num_discard: int,
    ) -> list[Card]:
        cards = self.sort_for_discard(valid_cards, player.state.actions, player, game)
        cards = cards[:num_discard]
        return cards

    def smugglers(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        card = max(valid_cards, key=lambda card: card.get_cost(player, game))
        return card

    def tide_pools(
            self,
            player: "Player",
            game: "Game",
            valid_cards: list[Card],
            num_discard: int,
    ) -> list[Card]:
        actions = player.state.actions
        cards = self.sort_for_discard(valid_cards, actions, player, game)
        cards = cards[:num_discard]
        return cards

    def treasury(
        self,
        prompt: str,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None,
    ) -> bool:
        return True

    def warehouse(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
        num_discard: int,
    ) -> list[Card]:
        cards = self.sort_for_discard(valid_cards, player.state.actions, player, game)
        cards = cards[:num_discard]
        return cards

    def alchemist(
        self,
        player: "Player",
        game: "Game",
    ) -> bool:
        return True

    def apothecary(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> list[Card]:
        cards = sorted(
            valid_cards,
            key=lambda card: card.get_cost(player, game),
        )
        return cards

    def apprentice(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        trash_cards = self.determine_trash_cards(valid_cards, player, game, required=True)
        return trash_cards[0]

    def golem(
        self,
        player: "Player",
        game: "Game",
    ) -> int:
        return 0

    def herbalist(
        self,
        player: "Player",
        game: "Game",
        card: Card,
    ) -> bool:
        return card.name != "Copper"

    def scrying_pool(
        self,
        prompt: str,
        player: "Player",
        game: "Game",
        relevant_cards: list[Card],
    ) -> bool:
        card = relevant_cards[0]
        if "your" in prompt:
            return CardType.Action not in card.type
        else:
            return not (
                (CardType.Victory in card.type and len(card.type) == 1) or
                card.name in {"Copper", "Curse"}
            )

    def transmute(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        trash_cards = self.determine_trash_cards(valid_cards, player, game, required=True)
        return trash_cards[0]

    def university_binary(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card]|None,
    ) -> bool:
        return True

    def university_gain(
        self,
        player: "Player",
        game: "Game",
        valid_cards: list[Card],
    ) -> Card:
        card = max(valid_cards, key=lambda c: c.get_cost(player, game))
        return card


class OptimizedBot(Bot):
    """
    Bot with logic for playing and reacting to all cards.

    """

    def __init__(
        self,
        decider: Decider|None = None,
        player_id: str = "bot",
    ):
        decider = decider if decider else OptimizedBotDecider()
        super().__init__(decider=decider, player_id=player_id)
