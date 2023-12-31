from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game
    from pyminion.player import Player


EffectHandler = Callable[["Player", "Card", "Game"], None]

class EffectRegistry:
    def __init__(self):
        self.turn_on_play_handlers: List[EffectHandler] = []
        self.persistent_on_play_handlers: List[EffectHandler] = []
        self.on_gain_handlers: List[EffectHandler] = []
        self.on_buy_handlers: List[EffectHandler] = []

    def end_turn(self) -> None:
        self.turn_on_play_handlers.clear()

    def register_on_play_handler(self, handler: EffectHandler, one_turn: bool = False) -> None:
        if one_turn:
            self.turn_on_play_handlers.append(handler)
        else:
            self.persistent_on_play_handlers.append(handler)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        for handler in self.turn_on_play_handlers:
            handler(player, card, game)

        for handler in self.persistent_on_play_handlers:
            handler(player, card, game)

    def register_on_gain_handler(self, handler: EffectHandler) -> None:
        self.on_gain_handlers.append(handler)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        for handler in self.on_gain_handlers:
            handler(player, card, game)

    def on_buy(self, player: "Player", card: "Card", game: "Game") -> None:
        for handler in self.on_gain_handlers:
            handler(player, card, game)
        for handler in self.on_buy_handlers:
            handler(player, card, game)
