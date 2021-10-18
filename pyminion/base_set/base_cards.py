from pyminion.models.cards import Treasure, Victory, Smithy, Village, Market, Laboratory
from pyminion.models.base import Pile

COPPER = 60
SILVER = 40
GOLD = 30
VICTORY = 8

START_COPPER = 7
START_ESTATE = 3

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


copper_pile = Pile([copper for x in range(COPPER)])
silver_pile = Pile([silver for x in range(SILVER)])
gold_pile = Pile([copper for x in range(GOLD)])
estate_pile = Pile([estate for x in range(VICTORY)])
duchy_pile = Pile([duchy for x in range(VICTORY)])
province_pile = Pile([province for x in range(VICTORY)])

core_supply = [
    copper_pile,
    silver_pile,
    gold_pile,
    estate_pile,
    duchy_pile,
    province_pile,
]


start_cards = [copper for x in range(START_COPPER)] + [
    estate for x in range(START_ESTATE)
]
