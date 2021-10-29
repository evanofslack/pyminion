from pyminion.util import pile_maker, kingdom_maker
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
    cellar,
    chapel,
    workshop,
)
from pyminion.models.core import Deck

COPPER_PILE = 60
SILVER_PILE = 40
GOLD_PILE = 30
VICTORY_PILE = 8

copper_pile = pile_maker(card=copper, num_card=COPPER_PILE)
silver_pile = pile_maker(card=silver, num_card=SILVER_PILE)
gold_pile = pile_maker(card=gold, num_card=GOLD_PILE)
estate_pile = pile_maker(card=estate, num_card=VICTORY_PILE)
duchy_pile = pile_maker(card=duchy, num_card=VICTORY_PILE)
province_pile = pile_maker(card=province, num_card=VICTORY_PILE)


core_supply = [
    copper_pile,
    silver_pile,
    gold_pile,
    estate_pile,
    duchy_pile,
    province_pile,
]

KINGDOM_PILE = 10
kingdom_cards = kingdom_maker(
    cards=[
        smithy,
        village,
        market,
        laboratory,
        moneylender,
        cellar,
        chapel,
        workshop,
    ],
    pile_length=KINGDOM_PILE,
)


START_COPPER = 7
START_ESTATE = 3
start_cards = [copper] * START_COPPER + [estate] * START_ESTATE
start_deck = Deck(cards=start_cards)
