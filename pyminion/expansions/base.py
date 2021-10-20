from pyminion.models.cards import Treasure, Victory

from pyminion.models.base import (
    copper,
    silver,
    gold,
    estate,
    duchy,
    province,
    smithy,
    village,
    laboratory,
    market,
    moneylender,
)
from pyminion.models.core import Pile, Card
from typing import List

COPPER = 60
SILVER = 40
GOLD = 30
VICTORY = 8

START_COPPER = 7
START_ESTATE = 3
PILE_LENGTH = 10


def pile_maker(card: Card, num_card: int) -> Pile:
    return Pile([card for x in range(num_card)])


def kingdom_maker(cards: List[Card]) -> List[Pile]:
    return [pile_maker(card, PILE_LENGTH) for card in cards]


copper_pile = pile_maker(card=copper, num_card=COPPER)
silver_pile = pile_maker(card=silver, num_card=SILVER)
gold_pile = pile_maker(card=gold, num_card=GOLD)
estate_pile = pile_maker(card=estate, num_card=VICTORY)
duchy_pile = pile_maker(card=duchy, num_card=VICTORY)
province_pile = pile_maker(card=province, num_card=VICTORY)


core_supply = [
    copper_pile,
    silver_pile,
    gold_pile,
    estate_pile,
    duchy_pile,
    province_pile,
]


kingdom_cards = kingdom_maker(cards=[smithy, village, market, laboratory, moneylender])


start_cards = [copper for x in range(START_COPPER)] + [
    estate for x in range(START_ESTATE)
]
