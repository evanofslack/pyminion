import functools
import logging
from collections import Counter
from typing import Callable, List, Optional, Tuple, Type, Union

from pyminion.core import Card
from pyminion.exceptions import (InvalidBinaryInput, InvalidMultiCardInput,
                                 InvalidSingleCardInput)

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
) -> Optional[List[Card]]:
    """
    Get user input when given the option to select multiple cards

    valid_cards are a list of cards that a user can choose from. For example,
    when prompting a user to trash cards from their hand, valid cards would
    be the user's hand.

    Raise exception if user provided selection is not in valid_cards.

    """
    card_input = input(prompt)
    if not card_input:
        return None
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
