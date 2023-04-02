import functools
import logging
from collections import Counter
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple, Type, Union

from pyminion.core import (CardType, Card, Deck)
from pyminion.exceptions import (InsufficientMoney, InvalidBinaryInput,
                                 InvalidMultiCardInput, InvalidSingleCardInput)
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


def validate_input(
    func: Optional[Callable] = None,
    exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]] = (),
):
    """
    Decorator to ensure that a user enters valid input when prompted.
    If input is invalid, the error is printed to the terminal and the user is prompted again

    Accepts a tuple of exceptions to catch

    """
    assert callable(func) or func is None

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.error(e)

        return wrapper

    return decorator(func) if callable(func) else decorator


def binary_decision(prompt: str) -> bool:
    """
    Get user response to a binary question.
    Raise exception is input is anything other than 'yes' or 'no'

    """

    decision = input(prompt)
    if decision in ("yes", "y", "Yes", "Y"):
        return True
    elif decision in ("no", "n", "No", "N"):
        return False
    else:
        raise InvalidBinaryInput("Invalid response, valid choices are 'yes' or 'no'")


def single_card_decision(
    prompt: str, valid_cards: List[Card], valid_mixin: str = "placeholder"
) -> Optional[Union[Card, str]]:
    """
    Get user input when given the option to select one card

    valid_cards are a list of cards that a user can choose from. For example,
    when prompting a user to discard a card from their hand, valid cards would
    be the user's hand.

    valid_mixin allows for options other than a card to be selected. For example,
    "all" mixin would be used to autoplay treasures when prompting treasures to play

    Raise exception if user provided selection is not in valid_cards and is not
    a valid_mixin.

    """
    card_input = input(prompt)
    if not card_input:
        return None

    if card_input == valid_mixin:
        return valid_mixin

    for card in valid_cards:
        if card_input.casefold() == card.name.casefold():
            return card

    raise InvalidSingleCardInput(
        f"Invalid input, {card_input} is not a valid selection"
    )


def multiple_card_decision(
    prompt: str, valid_cards: List[Card]
) -> List[Card]:
    """
    Get user input when given the option to select multiple cards

    valid_cards are a list of cards that a user can choose from. For example,
    when prompting a user to trash cards from their hand, valid cards would
    be the user's hand.

    Raise exception if user provided selection is not in valid_cards.

    """
    card_input = input(prompt)
    if not card_input:
        return []
    card_strings = [x.strip() for x in card_input.split(",")]
    selected_cards = []
    for card_string in card_strings:
        for card in valid_cards:
            if card_string.casefold() == card.name.casefold():
                selected_cards.append(card)
                break
        else:
            raise InvalidMultiCardInput(
                f"Invalid input, {card_string} is not a valid card"
            )

    selected_count = Counter(selected_cards)
    valid_count = Counter(valid_cards)

    for element in selected_count:
        if selected_count[element] > valid_count[element]:
            raise InvalidMultiCardInput(
                f"Invalid input, attempted to select too many copies of {element}"
            )
    return selected_cards


class HumanDecider:
    """
    Prompts human for decisions through the terminal.

    """

    @validate_input(exceptions=InvalidBinaryInput)
    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List[Card]] = None,
    ) -> bool:
        """
        Wrap binary_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return binary_decision(prompt=prompt)

    @validate_input(exceptions=InvalidMultiCardInput)
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

        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_discard:
            raise InvalidMultiCardInput(
                f"Invalid response, you must discard at least {min_num_discard} card(s)"
            )
        elif max_num_discard >= 0 and len_result > max_num_discard:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot discard more than {max_num_discard} card(s)"
            )

        return result

    @validate_input(exceptions=InvalidMultiCardInput)
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

        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_trash:
            raise InvalidMultiCardInput(
                f"Invalid response, you must trash at least {min_num_trash} card(s)"
            )
        elif max_num_trash >= 0 and len_result > max_num_trash:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot trash more than {max_num_trash} card(s)"
            )

        return result

    @validate_input(exceptions=InvalidMultiCardInput)
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
        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_gain:
            raise InvalidMultiCardInput(
                f"Invalid response, you must gain at least {min_num_gain} card(s)"
            )
        elif max_num_gain >= 0 and len_result > max_num_gain:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot gain more than {max_num_gain} card(s)"
            )

        return result

    @validate_input(exceptions=InvalidMultiCardInput)
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
        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_topdeck:
            raise InvalidMultiCardInput(
                f"Invalid response, you must topdeck at least {min_num_topdeck} card(s)"
            )
        elif max_num_topdeck >= 0 and len_result > max_num_topdeck:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot topdeck more than {max_num_topdeck} card(s)"
            )

        return result

    @validate_input(exceptions=InvalidSingleCardInput)
    def multi_play_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        required: bool = True,
    ) -> Optional["Card"]:
        result = single_card_decision(prompt, valid_cards)

        if isinstance(result, str):
            raise InvalidSingleCardInput(
                f"Invalid response, you must name a valid card"
            )
        elif required and result is None:
            raise InvalidSingleCardInput(
                f"Invalid response, you must name a valid card"
            )

        return result


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
        super().__init__(decider=HumanDecider(), deck=deck, player_id=player_id)

    def start_action_phase(self, game: "Game") -> None:
        while self.state.actions:

            viable_actions = [card for card in self.hand.cards if CardType.Action in card.type]
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
        viable_treasures = [card for card in self.hand.cards if CardType.Treasure in card.type]
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
