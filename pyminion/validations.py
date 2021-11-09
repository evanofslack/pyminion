from collections import Counter
from typing import List

from pyminion.exceptions import InvalidMultiCardInput, InvalidSingleCardInput
from pyminion.models.core import Card


def single_card_validation(target_card: Card, valid_cards: List[Card]) -> bool:
    if target_card in valid_cards:
        return True

    raise InvalidSingleCardInput(
        f"Invalid input, {target_card} is not a valid selection"
    )


def multiple_card_validation(target_cards: List[Card], valid_cards: List[Card]) -> bool:

    for target_card in target_cards:
        if target_card not in valid_cards:
            raise InvalidMultiCardInput(
                f"Invalid input, {target_card} is not a valid card"
            )

    target_count = Counter(target_cards)
    valid_count = Counter(valid_cards)

    for element in target_count:
        if target_count[element] > valid_count[element]:
            raise InvalidMultiCardInput(
                f"Invalid input, attempted to drop too many copies of {element}"
            )

    return True
