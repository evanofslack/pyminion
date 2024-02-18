from typing import TYPE_CHECKING, Callable, List, Union

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
        self.buy_effects: List[PlayerCardGameEffect] = []
        self.discard_effects: List[PlayerCardGameEffect] = []
        self.draw_effects: List[PlayerCardGameEffect] = []
        self.gain_effects: List[PlayerCardGameEffect] = []
        self.play_effects: List[PlayerCardGameEffect] = []
        self.shuffle_effects: List[PlayerGameEffect] = []
        self.turn_start_effects: List[PlayerGameEffect] = []
        self.turn_end_effects: List[PlayerGameEffect] = []

    def _unregister_effects(self, name: str, effect_list: Union[List[PlayerGameEffect], List[PlayerCardGameEffect]]) -> None:
        i = 0
        while i < len(effect_list):
            effect = effect_list[i]
            if effect.name == name:
                effect_list.pop(i)
            else:
                i += 1

    def on_buy(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.gain_effects:
            effect.handler(player, card, game)
        for effect in self.buy_effects:
            effect.handler(player, card, game)

    def on_discard(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.discard_effects:
            effect.handler(player, card, game)

    def on_draw(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.draw_effects:
            effect.handler(player, card, game)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.gain_effects:
            effect.handler(player, card, game)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        for effect in self.play_effects:
            effect.handler(player, card, game)

    def on_shuffle(self, player: "Player", game: "Game") -> None:
        for effect in self.shuffle_effects:
            effect.handler(player, game)

    def on_turn_start(self, player: "Player", game: "Game") -> None:
        for effect in self.turn_start_effects:
            effect.handler(player, game)

    def on_turn_end(self, player: "Player", game: "Game") -> None:
        for effect in self.turn_end_effects:
            effect.handler(player, game)

    def register_buy_effect(self, effect: PlayerCardGameEffect) -> None:
        self.buy_effects.append(effect)

    def unregister_buy_effects(self, name: str) -> None:
        self._unregister_effects(name, self.buy_effects)

    def register_discard_effect(self, effect: PlayerCardGameEffect) -> None:
        self.discard_effects.append(effect)

    def unregister_discard_effects(self, name: str) -> None:
        self._unregister_effects(name, self.discard_effects)

    def register_draw_effect(self, effect: PlayerCardGameEffect) -> None:
        self.draw_effects.append(effect)

    def unregister_draw_effects(self, name: str) -> None:
        self._unregister_effects(name, self.draw_effects)

    def register_gain_effect(self, effect: PlayerCardGameEffect) -> None:
        self.gain_effects.append(effect)

    def unregister_gain_effects(self, name: str) -> None:
        self._unregister_effects(name, self.gain_effects)

    def register_play_effect(self, effect: PlayerCardGameEffect) -> None:
        self.play_effects.append(effect)

    def unregister_play_effects(self, name: str) -> None:
        self._unregister_effects(name, self.play_effects)

    def register_shuffle_effect(self, effect: PlayerGameEffect) -> None:
        self.shuffle_effects.append(effect)

    def unregister_shuffle_effects(self, name: str) -> None:
        self._unregister_effects(name, self.shuffle_effects)

    def register_turn_start_effect(self, effect: PlayerGameEffect) -> None:
        self.turn_start_effects.append(effect)

    def unregister_turn_start_effects(self, name: str) -> None:
        self._unregister_effects(name, self.turn_start_effects)

    def register_turn_end_effect(self, effect: PlayerGameEffect) -> None:
        self.turn_end_effects.append(effect)

    def unregister_turn_end_effects(self, name: str) -> None:
        self._unregister_effects(name, self.turn_end_effects)
