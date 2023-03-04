"""
Contains an Enum class for all card types that are currently used in the implemented expansions

"""

from enum import Enum

class CardType(Enum):
    Treasure = 1
    Victory = 2
    Curse = 3
    Action = 4
    Attack = 5
    Reaction = 6