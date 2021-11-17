from pyminion.models.base import (
    artisan,
    bandit,
    bureaucrat,
    cellar,
    chapel,
    copper,
    council_room,
    curse,
    duchy,
    estate,
    festival,
    gold,
    harbinger,
    laboratory,
    market,
    merchant,
    moat,
    moneylender,
    poacher,
    province,
    silver,
    smithy,
    throne_room,
    vassal,
    village,
    witch,
    workshop,
)

START_COPPER = 7
START_ESTATE = 3
start_cards = [copper] * START_COPPER + [estate] * START_ESTATE

base_cards = [
    artisan,
    bandit,
    bureaucrat,
    cellar,
    chapel,
    council_room,
    festival,
    harbinger,
    laboratory,
    market,
    merchant,
    moat,
    moneylender,
    poacher,
    smithy,
    throne_room,
    vassal,
    village,
    witch,
    workshop,
]

basic_cards = [copper, silver, gold, estate, duchy, province, curse]
