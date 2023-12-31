from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game
    from pyminion.player import Player


EffectHandler = Callable[["Player", "Card", "Game"], None]


class Effect:
    def __init__(self, name: str, handler: EffectHandler):
        self.name = name
        self.handler = handler


class EffectRegistry:
    def __init__(self):
        self.turn_on_play_effects: List[Effect] = []
        self.persistent_on_play_effects: List[Effect] = []
        self.on_gain_effects: List[Effect] = []
        self.on_buy_effects: List[Effect] = []

    def end_turn(self) -> None:
        self.turn_on_play_effects.clear()

    def register_on_play_handler(self, effect: Effect, one_turn: bool = False) -> None:
        if one_turn:
            self.turn_on_play_effects.append(effect)
        else:
            self.persistent_on_play_effects.append(effect)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.turn_on_play_effects:
            effect.handler(player, card, game)

        for effect in self.persistent_on_play_effects:
            effect.handler(player, card, game)

    def register_on_gain_handler(self, effect: Effect) -> None:
        self.on_gain_effects.append(effect)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.on_gain_effects:
            effect.handler(player, card, game)

    def on_buy(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.on_gain_effects:
            effect.handler(player, card, game)
        for effect in self.on_buy_effects:
            effect.handler(player, card, game)
