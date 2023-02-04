import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Union

from pyminion.core import (AbstractDeck, Card, Deck, DiscardPile, Hand,
                           Playmat, Supply, Trash)
from pyminion.decisions import (binary_decision, multiple_card_decision,
                                single_card_decision, validate_input)
from pyminion.exceptions import (CardNotFound, EmptyPile, InsufficientBuys,
                                 InsufficientMoney, InvalidBinaryInput,
                                 InvalidCardPlay, InvalidMultiCardInput,
                                 InvalidSingleCardInput)

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


@dataclass
class State:
    """
    Hold state during a player's turn

    """

    actions: int = 1
    money: int = 0
    buys: int = 1


class Player:
    """
    Basic representation of a player including the piles of cards they own
    and the basic actions they can take to manipulate the state of the game.

    """

    def __init__(
        self,
        deck: Optional[Deck] = None,
        discard_pile: Optional[DiscardPile] = None,
        hand: Optional[Hand] = None,
        playmat: Optional[Playmat] = None,
        state: Optional[State] = None,
        player_id: str = "",
    ):
        self.deck = deck if deck else Deck()
        self.discard_pile = discard_pile if discard_pile else DiscardPile()
        self.hand = hand if hand else Hand()
        self.playmat = playmat if playmat else Playmat()
        self.state = state if state else State()
        self.player_id = player_id
        self.turns: int = 0
        self.shuffles: int = 0

    def __repr__(self):
        return f"{self.player_id}"

    def reset(self):
        """
        Reset the state of the player to a pre-game state.
        Required for resetting player deck and state between games when running simulations.

        """
        self.turns = 0
        self.shuffles = 0
        self.deck.cards = []
        self.discard_pile.cards = []
        self.hand.cards = []

    def draw(
        self,
        num_cards: int = 1,
        destination: Optional[AbstractDeck] = None,
        silent: bool = False,
    ) -> None:
        """
        Draw cards from deck and add them to the specified destination.
        Defaults to drawing one card and adding to the player's hand.

        By default, drawn cards and deck shuffles are logged.
        Call with silent = True to disable logging of drawn cards

        """
        if destination is None:
            destination = self.hand
        drawn_cards: AbstractDeck = AbstractDeck()
        for _ in range(num_cards):
            # Both deck and discard empty -> do nothing
            if len(self.discard_pile) == 0 and len(self.deck) == 0:
                pass
            # Deck is empty -> shuffle discard pile into deck
            elif len(self.deck) == 0:
                logger.info(f"{self} shuffles their deck")
                self.discard_pile.move_to(self.deck)
                self.deck.shuffle()
                self.shuffles += 1
                draw_card = self.deck.draw()
                destination.add(draw_card)
                drawn_cards.add(draw_card)
            else:
                draw_card = self.deck.draw()
                destination.add(draw_card)
                drawn_cards.add(draw_card)
        if not silent:
            logger.info(f"{self} draws {drawn_cards}")

    def discard(self, target_card: Card) -> None:
        """
        Move specified card from the player's hand to the player's discard pile.

        """
        for card in self.hand.cards:
            if card == target_card:
                self.discard_pile.add(self.hand.remove(card))
                logger.info(f"{self} discards {card}")
                return

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        """
        Find target card in player's hand and play it.

        If generic_play is true, card is moved from player's hand to playmat
        and player action count decreased by 1. This is the default behavior
        but is overridden for cards like vassal and throne room.

        """
        if target_card not in self.hand.cards:
            raise CardNotFound(f"Invalid play, {target_card} not in hand")
        for card in self.hand.cards:
            if card.name == target_card.name:
                if "Action" in card.type:
                    card.play(player=self, game=game, generic_play=generic_play)
                    return
                if "Treasure" in card.type:
                    card.play(player=self, game=game)
                    return
        raise InvalidCardPlay(f"Invalid play, {target_card} could not be played")

    def exact_play(self, card: Card, game: "Game", generic_play: bool = True) -> None:
        """
        Similar to previous play method, except exact card to play must be specified.
        This is method is necessary when playing cards not in the player's hand, such as vassal.

        """
        if "Action" in card.type:
            card.play(player=self, game=game, generic_play=generic_play)
        elif "Treasure" in card.type:
            card.play(player=self, game=game)
        else:
            raise InvalidCardPlay(f"Unable to play {card} with type {card.type}")

    def buy(self, card: Card, supply: "Supply") -> None:
        """
        Buy a card from the supply and add to player's discard pile.
        Check that player has sufficient money and buys to gain the card.

        """
        assert isinstance(card, Card)
        if card.cost > self.state.money:
            raise InsufficientMoney(
                f"{self.player_id}: Not enough money to buy {card.name}"
            )
        if self.state.buys < 1:
            raise InsufficientBuys(
                f"{self.player_id}: Not enough buys to buy {card.name}"
            )
        try:
            supply.gain_card(card)
        except EmptyPile as e:
            raise e
        self.state.money -= card.cost
        self.state.buys -= 1
        self.discard_pile.add(card)
        logger.info(f"{self} buys {card}")

    def gain(
        self, card: Card, supply: "Supply", destination: Optional[AbstractDeck] = None
    ) -> None:
        """
        Gain a card from the supply and add to destination.
        Defaults to adding the card to the player's discard pile.

        """
        if destination is None:
            destination = self.discard_pile

        gain_card = supply.gain_card(card)
        destination.add(gain_card)
        logger.info(f"{self} gains {gain_card}")

    def trash(self, target_card: Card, trash: "Trash") -> None:
        """
        Move card from player's hand to the trash.

        """
        for card in self.hand.cards:
            if card == target_card:
                trash.add(self.hand.remove(card))
                logger.info(f"{self} trashes {card}")

                break

    def autoplay_treasures(
        self, viable_treasures: Optional[List[Card]], game: "Game"
    ) -> None:
        """
        Play all treasures in hand

        """
        if not viable_treasures:
            return

        i = 0
        while i < len(viable_treasures):
            self.exact_play(viable_treasures[i], game)
            viable_treasures.remove(viable_treasures[i])

    def start_turn(self) -> None:
        """
        Increase turn counter and reset state

        """
        self.turns += 1
        self.state.actions = 1
        self.state.money = 0
        self.state.buys = 1

    def start_cleanup_phase(self):
        """
        Move hand and playmat cards into discard pile and draw 5 new cards.

        """
        self.discard_pile.cards += self.hand.cards
        self.discard_pile.cards += self.playmat.cards
        self.hand.cards = []
        self.playmat.cards = []
        self.draw(5)
        self.state.actions = 1
        self.state.money = 0
        self.state.buys = 1

    def get_all_cards(self) -> List[Card]:
        """
        Get a list of all the cards the player has in their possesion.

        """
        all_cards = (
            self.deck.cards
            + self.discard_pile.cards
            + self.playmat.cards
            + self.hand.cards
        )
        return all_cards

    def get_card_count(self, card: Card) -> int:
        """
        Get count of a specific card in player's whole deck.

        """
        return self.get_all_cards().count(card)

    def get_victory_points(self) -> int:
        """
        Return the number of victory points a player has.

        """
        total_vp: int = 0
        for card in self.get_all_cards():
            if "Victory" in card.type or "Curse" in card.type:
                total_vp += card.score(self)
        return total_vp

    def get_treasure_money(self) -> int:
        """
        Return the amount of money a player has in their deck from treasure cards.

        """
        total_money: int = 0
        for card in self.get_all_cards():
            if "Treasure" in card.type:
                total_money += card.money
        return total_money

    def get_action_money(self) -> int:
        """
        Return the amount of money a player has in their deck from action cards.

        """
        total_money: int = 0
        for card in self.get_all_cards():
            if "Action" in card.type:
                total_money += card.money
        return total_money

    def get_deck_money(self) -> int:
        """
        Return total count of all money a player has in their deck.

        """
        treasure_money = self.get_treasure_money()
        action_money = self.get_action_money()
        return treasure_money + action_money


class Human(Player):
    """
    Human player can make choices as to which cards
    to play and buy in real time through the terminal

    """

    def __init__(
        self,
        deck: Optional[Deck] = None,
        player_id: str = "human",
    ):
        super().__init__(deck=deck, player_id=player_id)

    @staticmethod
    @validate_input(exceptions=InvalidBinaryInput)
    def binary_decision(prompt: str) -> bool:
        """
        Wrap binary_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return binary_decision(prompt=prompt)

    @staticmethod
    @validate_input(exceptions=InvalidSingleCardInput)
    def single_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[Union[Card, str]]:
        """
        Wrap single_card_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """

        return single_card_decision(prompt=prompt, valid_cards=valid_cards)

    @staticmethod
    @validate_input(exceptions=InvalidMultiCardInput)
    def multiple_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[List[Card]]:
        """
        Wrap multiple_card_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return multiple_card_decision(prompt=prompt, valid_cards=valid_cards)

    def is_attacked(self, player: Player, attack_card: Card) -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                block = self.binary_decision(
                    prompt=f"Would you like to block {player.player_id}'s {attack_card} with your Moat? y/n: "
                )
                return not block
        return True

    def start_action_phase(self, game: "Game") -> None:
        while self.state.actions:

            viable_actions = [card for card in self.hand.cards if "Action" in card.type]
            if not viable_actions:
                return

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_action(game: "Game") -> None:
                logger.info(f"Hand: {self.hand}")
                card = single_card_decision(
                    prompt="Choose an action card to play: ",
                    valid_cards=viable_actions,
                )
                if not card or isinstance(card, str):
                    return
                self.play(card, game)
                return

            choose_action(game)

    def start_treasure_phase(self, game: "Game") -> None:
        viable_treasures = [card for card in self.hand.cards if "Treasure" in card.type]
        while viable_treasures:

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_treasure(game: "Game") -> None:
                logger.info(f"Hand: {self.hand}")
                response = single_card_decision(
                    prompt="Choose an treasure card to play or 'all' to autoplay treasures: ",
                    valid_cards=viable_treasures,
                    valid_mixin="all",
                )
                if response == "all":
                    self.autoplay_treasures(
                        viable_treasures=viable_treasures, game=game
                    )
                    return
                if not response or isinstance(response, str):
                    return
                self.exact_play(response, game)
                logger.info(f"{self.player_id} played {response}")
                viable_treasures.remove(response)

            choose_treasure(game)

    def start_buy_phase(self, game: "Game") -> None:
        while self.state.buys:
            logger.info(f"\nSupply:{game.supply}")
            logger.info(f"Money: {self.state.money}")
            logger.info(f"Buys: {self.state.buys}")

            @validate_input(exceptions=(InvalidSingleCardInput, InsufficientMoney))
            def choose_buy(game: "Game") -> None:
                card = single_card_decision(
                    prompt="Choose a card to buy: ",
                    valid_cards=game.supply.avaliable_cards(),
                )
                if not card or isinstance(card, str):
                    return
                self.buy(card, game.supply)

            choose_buy(game)

    def take_turn(self, game: "Game") -> None:
        self.start_turn()
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()
