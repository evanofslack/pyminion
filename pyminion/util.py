from pyminion.models.core import Card, Pile
from pyminion.exceptions import InvalidBinaryInput, InvalidMultiCardInput

from typing import List, Optional
from collections import Counter

# TODO write tests
def pile_maker(card: Card, num_card: int) -> Pile:
    return Pile([card for x in range(num_card)])


# TODO write tests
def kingdom_maker(cards: List[Card], pile_length: int) -> List[Pile]:
    return [pile_maker(card, pile_length) for card in cards]


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
            f"Invalid input, {card_strings[0]} does not match any card in your hand"
        )

    # TODO This can be abstracted into function
    selected_count = Counter(selected_cards)
    valid_count = Counter(valid_cards)

    for element in selected_count:
        if selected_count[element] > valid_count[element]:
            raise InvalidMultiCardInput(
                f"Invalid input, attemped to drop too many copies of {element}"
            )
    return selected_cards
