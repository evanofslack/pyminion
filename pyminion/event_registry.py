from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game
    from pyminion.player import Player


class EventRegistry:
    def __init__(self):
        self.on_play_handlers: List[Callable[["Player", "Card", "Game"], None]] = []

    def register_on_play_handler(self, handler: Callable[["Player", "Card", "Game"], None]) -> None:
        self.on_play_handlers.append(handler)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        for handler in self.on_play_handlers:
            handler(player, card, game)
