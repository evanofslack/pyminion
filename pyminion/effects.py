from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game
    from pyminion.player import Player


PlayerGameEffectHandler = Callable[["Player", "Game"], None]
PlayerCardGameEffectHandler = Callable[["Player", "Card", "Game"], None]


class PlayerGameEffect:
    def __init__(self, name: str, handler: PlayerGameEffectHandler):
        self.name = name
        self.handler = handler


class PlayerCardGameEffect:
    def __init__(self, name: str, handler: PlayerCardGameEffectHandler):
        self.name = name
        self.handler = handler


class EffectRegistry:
    def __init__(self):
        self.turn_play_effects: List[PlayerCardGameEffect] = []
        self.persistent_play_effects: List[PlayerCardGameEffect] = []
        self.gain_effects: List[PlayerCardGameEffect] = []
        self.buy_effects: List[PlayerCardGameEffect] = []
        self.shuffle_effects: List[PlayerGameEffect] = []

    def end_turn(self) -> None:
        self.turn_play_effects.clear()

    def on_buy(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.gain_effects:
            effect.handler(player, card, game)
        for effect in self.buy_effects:
            effect.handler(player, card, game)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.gain_effects:
            effect.handler(player, card, game)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.turn_play_effects:
            effect.handler(player, card, game)

        for effect in self.persistent_play_effects:
            effect.handler(player, card, game)

    def on_shuffle(self, player: "Player", game: "Game") -> None:
        for effect in self.shuffle_effects:
            effect.handler(player, game)

    def register_gain_effect(self, effect: PlayerCardGameEffect) -> None:
        self.gain_effects.append(effect)

    def register_play_effect(self, effect: PlayerCardGameEffect, one_turn: bool = False) -> None:
        if one_turn:
            self.turn_play_effects.append(effect)
        else:
            self.persistent_play_effects.append(effect)

    def register_shuffle_effect(self, effect: PlayerGameEffect) -> None:
        self.shuffle_effects.append(effect)
