import logging
from typing import TYPE_CHECKING

from pyminion.core import (
    CardType,
    Treasure,
)
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Potion(Treasure):
    def __init__(self):
        super().__init__("Potion", 4, (CardType.Treasure,), 0)

    def play(self, player: Player, game: "Game") -> None:
        super().play(player, game)

        player.state.potions += 1


potion = Potion()
