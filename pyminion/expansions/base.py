from pyminion.models.cards import Treasure, Victory

from pyminion.models.base import (
    Smithy,
    Village,
    Market,
    Laboratory,
    Moneylender,
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

# Treasures
copper = Treasure(name="Copper", cost=0, money=1)
silver = Treasure(name="Silver", cost=3, money=2)
gold = Treasure(name="Gold", cost=6, money=3)

# Victory
estate = Victory(name="Estate", cost=2, victory_points=1)
duchy = Victory(name="Duchy", cost=5, victory_points=3)
province = Victory(name="Province", cost=8, victory_points=6)


# Actions
smithy = Smithy()
village = Village()
market = Market()
laboratory = Laboratory()
moneylender = Moneylender()


def pile_maker(card: Card, num_card: int) -> Pile:
    return Pile([card for x in range(num_card)])


def kingdom_maker(cards: List[Card]) -> List[Pile]:
    return [pile_maker(card, PILE_LENGTH) for card in cards]


# copper_pile = Pile([copper for x in range(COPPER)])
# silver_pile = Pile([silver for x in range(SILVER)])
# gold_pile = Pile([gold for x in range(GOLD)])
# estate_pile = Pile([estate for x in range(VICTORY)])
# duchy_pile = Pile([duchy for x in range(VICTORY)])
# province_pile = Pile([province for x in range(VICTORY)])

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
