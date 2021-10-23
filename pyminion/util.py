from pyminion.models.core import Card, Pile
from typing import List


# TODO write tests
def pile_maker(card: Card, num_card: int) -> Pile:
    return Pile([card for x in range(num_card)])


# TODO write tests
def kingdom_maker(cards: List[Card], pile_length: int) -> List[Pile]:
    return [pile_maker(card, pile_length) for card in cards]
