from pyminion.models.base import (
    artisan,
    cellar,
    chapel,
    copper,
    curse,
    duchy,
    estate,
    festival,
    gold,
    harbinger,
    laboratory,
    market,
    moneylender,
    poacher,
    province,
    silver,
    smithy,
    vassal,
    village,
    workshop,
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
