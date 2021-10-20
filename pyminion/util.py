from pyminion.models.core import Card, Pile
from pyminion.exceptions import InvalidBinaryInput
from typing import List

# TODO write tests
def pile_maker(card: Card, num_card: int) -> Pile:
    return Pile([card for x in range(num_card)])


# TODO write tests
def kingdom_maker(cards: List[Card], pile_length: int) -> List[Pile]:
    return [pile_maker(card, pile_length) for card in cards]


def binary_decision(prompt: str) -> bool:
    while True:
        try:
            decision = input(prompt)
            if decision == "y":
                return True
            elif decision == "n":
                return False
            else:
                raise InvalidBinaryInput(
                    "Invalid response, valid choices are 'y' or 'n'"
                )
        except InvalidBinaryInput as e:
            print(e)
