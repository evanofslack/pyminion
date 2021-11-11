import functools
import logging
from collections import Counter
from typing import Callable, List, Optional, Tuple, Type, Union

from pyminion.exceptions import (
    InvalidBinaryInput,
    InvalidMultiCardInput,
    InvalidSingleCardInput,
)
from pyminion.models.core import Card

logger = logging.getLogger()


def validate_input(
    func: Callable = None, exceptions: Tuple[Type[Exception], ...] = Exception
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
    Get user response to a binary "yes" or "no" question.
    Raise exception is input is anything other than 'y' or 'n'

    """

    decision = input(prompt)
    if decision == "y":
        return True
    elif decision == "n":
        return False
    else:
        raise InvalidBinaryInput("Invalid response, valid choices are 'y' or 'n'")


def single_card_decision(
    prompt: str, valid_cards: List[Card], valid_mixin: str = "placeholder"
) -> Optional[Union[Card, str]]:
    """
    Get user response when given the option to select one card

    valid_mixin allows for options other than a card to be selected i.e. "auto"
    to autoplay treasures when deciding treasures to play

    Raise exception if user provided selection is not valid.

    """
    card_input = input(prompt)
    if not card_input:
        return False

    if card_input == valid_mixin:
        return valid_mixin

    selected_card = None
    for card in valid_cards:
        if card_input.casefold() == card.name.casefold():
            selected_card = card
            break

    if not selected_card:
        raise InvalidSingleCardInput(
            f"Invalid input, {card_input} is not a valid selection"
        )

    return selected_card


def multiple_card_decision(
    prompt: str, valid_cards: List[Card]
) -> Optional[List[Card]]:
    """
    Get user response when given the option to select multiple cards
    Raise exception if user provided selection is not valid.

    """
    card_input = input(prompt)
    if not card_input:
        return
    card_strings = [x.strip() for x in card_input.split(",")]
    selected_cards = []
    for card_string in card_strings:
        for card in valid_cards:
            # compare strings regardless of case i.e. 'Copper' = 'copper'
            if card_string.casefold() == card.name.casefold():
                selected_cards.append(card)
                break

    if not selected_cards:
        raise InvalidMultiCardInput(
            f"Invalid input, {card_strings[0]} is not a valid card"
        )

    selected_count = Counter(selected_cards)
    valid_count = Counter(valid_cards)

    for element in selected_count:
        if selected_count[element] > valid_count[element]:
            raise InvalidMultiCardInput(
                f"Invalid input, attempted to drop too many copies of {element}"
            )
    return selected_cards
