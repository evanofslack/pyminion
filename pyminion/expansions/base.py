from pyminion.util import pile_maker, kingdom_maker
from pyminion.models.base import (
    copper,
    silver,
    gold,
    estate,
    duchy,
    province,
    curse,
    smithy,
    village,
    laboratory,
    market,
    moneylender,
    cellar,
    chapel,
    workshop,
    festival,
    harbinger,
    vassal,
    artisan,
    poacher,
)


START_COPPER = 7
START_ESTATE = 3
start_cards = [copper] * START_COPPER + [estate] * START_ESTATE

base_cards = [
    smithy,
    village,
    market,
    laboratory,
    moneylender,
    cellar,
    chapel,
    workshop,
    festival,
    harbinger,
    vassal,
    artisan,
    poacher,
]

basic_cards = [copper, silver, gold, estate, duchy, province, curse]
