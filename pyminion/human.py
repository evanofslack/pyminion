import functools
import logging
from collections import Counter
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple, Type, Union

from pyminion.core import (CardType, Card, Deck)
from pyminion.exceptions import (InsufficientMoney, InvalidBinaryInput,
                                 InvalidMultiCardInput, InvalidMultiOptionInput,
                                 InvalidSingleCardInput, InvalidDeckPositionInput)
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
    prompt: str,
    valid_cards: List[Card],
    allow_all: bool = False,
) -> List[Card]:
    """
    Get user input when given the option to select multiple cards

    valid_cards are a list of cards that a user can choose from. For example,
    when prompting a user to trash cards from their hand, valid cards would
    be the user's hand.

    allow_all is a flag that, when True, allows the user to input "all" to
    return all valid cards.

    Raise exception if user provided selection is not in valid_cards.

    """
    card_input = input(prompt)
    if not card_input:
        return []

    if allow_all and card_input == "all":
        return valid_cards

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


def multiple_option_decision(
    options: List[str],
    num_choices: int = 1,
    unique: bool = True,
) -> List[int]:
    """
    Get user input when given multiple options

    options are a list of strings describing the options that a user can choose
    from.

    Raise exception if user provided selection is not a valid option

    """
    prompt = f"Choose {num_choices} of the following"
    if unique and num_choices > 1:
        prompt += " (the choices must be different)"
    prompt += ":"
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}: {option}")
    choice_input = input("Choice: ")
    choice_strings = [x.strip() for x in choice_input.split(",")]

    if len(choice_strings) != num_choices:
        raise InvalidMultiOptionInput("Invalid input, chose incorrect number of options")

    choices: List[int] = []
    for choice in choice_strings:
        try:
            choice_num = int(choice)
        except ValueError:
            raise InvalidMultiOptionInput(f"'{choice}' is not a valid number")

        if choice_num <= 0 or choice_num > len(options):
            raise InvalidMultiOptionInput(f"'{choice_num}' is not a valid option")

        choice_index = choice_num - 1
        if unique and choice_index in choices:
            raise InvalidMultiOptionInput("Choices are not unique")

        choices.append(choice_index)

    return choices


def deck_position_decision(prompt: str, num_deck_cards: int) -> int:
    pos_str = input(prompt).casefold()
    if pos_str == "top":
        pos = num_deck_cards
    elif pos_str == "bottom":
        pos = 0
    else:
        try:
            num = int(pos_str)
        except ValueError:
            raise InvalidDeckPositionInput(f"Invalid input, '{pos_str}' is not a valid position")

        max_num = num_deck_cards + 1
        if num < 1:
            raise InvalidDeckPositionInput(f"Invalid input, '{pos_str}' is less than the minimum value of 1")
        elif num > max_num:
            raise InvalidDeckPositionInput(f"Invalid input, '{pos_str}' is greater than the maximum value of {max_num}")

        pos = num - 1

    return pos


class HumanDecider:
    """
    Prompts human for decisions through the terminal.

    """

    @validate_input(exceptions=InvalidSingleCardInput)
    def action_phase_decision(
        self,
        valid_actions: List["Card"],
        player: "Player",
        game: "Game",
    ) -> Optional["Card"]:
        card = single_card_decision(
            prompt="Choose an action card to play: ",
            valid_cards=valid_actions,
        )
        if isinstance(card, str):
            raise InvalidSingleCardInput("You must choose a valid card")

        return card

    @validate_input(exceptions=InvalidMultiCardInput)
    def treasure_phase_decision(
        self,
        valid_treasures: List["Card"],
        player: "Player",
        game: "Game",
    ) -> List["Card"]:
        cards = multiple_card_decision(
            prompt="Choose treasures to play: ",
            valid_cards=valid_treasures,
            allow_all=True,
        )
        return cards

    @validate_input(exceptions=InvalidSingleCardInput)
    def buy_phase_decision(
        self,
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
    ) -> Optional["Card"]:
        card = single_card_decision(
            prompt="Choose a card to buy: ",
            valid_cards=valid_cards,
        )
        if isinstance(card, str):
            raise InvalidSingleCardInput("You must choose a valid card")

        return card

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

    @validate_input(exceptions=InvalidMultiOptionInput)
    def multiple_option_decision(
        self,
        card: "Card",
        options: List[str],
        player: "Player",
        game: "Game",
        num_choices: int = 1,
        unique: bool = True,
    ) -> List[int]:
        """
        Wrap multiple_option_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return multiple_option_decision(options, num_choices, unique)

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

    @validate_input(exceptions=InvalidDeckPositionInput)
    def deck_position_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        num_deck_cards: int,
    ) -> int:
        """
        Wrap deck_position_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return deck_position_decision(prompt, num_deck_cards)

    @validate_input(exceptions=InvalidMultiCardInput)
    def reveal_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_reveal: int = 0,
        max_num_reveal: int = -1,
    ) -> List["Card"]:
        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_reveal:
            raise InvalidMultiCardInput(
                f"Invalid response, you must reveal at least {min_num_reveal} card(s)"
            )
        elif max_num_reveal >= 0 and len_result > max_num_reveal:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot reveal more than {max_num_reveal} card(s)"
            )

        return result

    @validate_input(exceptions=InvalidMultiCardInput)
    def pass_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_pass: int = 0,
        max_num_pass: int = -1,
    ) -> List["Card"]:
        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_pass:
            raise InvalidMultiCardInput(
                f"Invalid response, you must pass at least {min_num_pass} card(s)"
            )
        elif max_num_pass >= 0 and len_result > max_num_pass:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot pass more than {max_num_pass} card(s)"
            )

        return result

    @validate_input(exceptions=InvalidMultiCardInput)
    def name_card_decision(
        self,
        prompt: str,
        card: "Card",
        valid_cards: List["Card"],
        player: "Player",
        game: "Game",
        min_num_name: int = 0,
        max_num_name: int = -1,
    ) -> List["Card"]:
        result = multiple_card_decision(prompt, valid_cards)
        len_result = len(result)

        if len_result < min_num_name:
            raise InvalidMultiCardInput(
                f"Invalid response, you must name at least {min_num_name} card(s)"
            )
        elif max_num_name >= 0 and len_result > max_num_name:
            raise InvalidMultiCardInput(
                f"Invalid response, you cannot name more than {max_num_name} card(s)"
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
