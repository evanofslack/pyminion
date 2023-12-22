from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game
    from pyminion.player import Player


EventHandler = Callable[["Player", "Card", "Game"], None]

class EventRegistry:
    def __init__(self):
        self.turn_on_play_handlers: List[EventHandler] = []
        self.persistent_on_play_handlers: List[EventHandler] = []
        self.on_gain_handlers: List[EventHandler] = []

    def end_turn(self) -> None:
        self.turn_on_play_handlers.clear()

    def register_on_play_handler(self, handler: EventHandler, one_turn: bool = False) -> None:
        if one_turn:
            self.turn_on_play_handlers.append(handler)
        else:
            self.persistent_on_play_handlers.append(handler)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        for handler in self.turn_on_play_handlers:
            handler(player, card, game)

        for handler in self.persistent_on_play_handlers:
            handler(player, card, game)

    def register_on_gain_handler(self, handler: EventHandler) -> None:
        self.on_gain_handlers.append(handler)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        for handler in self.on_gain_handlers:
            handler(player, card, game)
