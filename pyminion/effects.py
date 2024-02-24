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
    """
    Registery for effects to be triggered on various game events.

    """
    def __init__(self):
        self.buy_effects: List[PlayerCardGameEffect] = []
        self.discard_effects: List[PlayerCardGameEffect] = []
        self.draw_effects: List[PlayerCardGameEffect] = []
        self.gain_effects: List[PlayerCardGameEffect] = []
        self.play_effects: List[PlayerCardGameEffect] = []
        self.shuffle_effects: List[PlayerGameEffect] = []
        self.trash_effects: List[PlayerCardGameEffect] = []
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
        """
        Trigger buying effects.

        """
        for effect in self.gain_effects:
            effect.handler(player, card, game)
        for effect in self.buy_effects:
            effect.handler(player, card, game)

    def on_discard(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger discarding effects.

        """
        for effect in self.discard_effects:
            effect.handler(player, card, game)

    def on_draw(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger drawing effects.

        """
        for effect in self.draw_effects:
            effect.handler(player, card, game)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger gaining effects.

        """
        for effect in self.gain_effects:
            effect.handler(player, card, game)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger playing effects.

        """
        for effect in self.play_effects:
            effect.handler(player, card, game)

    def on_shuffle(self, player: "Player", game: "Game") -> None:
        """
        Trigger shuffling effects.

        """
        for effect in self.shuffle_effects:
            effect.handler(player, game)

    def on_trash(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger trashing effects.

        """
        for effect in self.trash_effects:
            effect.handler(player, card, game)

    def on_turn_start(self, player: "Player", game: "Game") -> None:
        """
        Trigger turn starting effects.

        """
        for effect in self.turn_start_effects:
            effect.handler(player, game)

    def on_turn_end(self, player: "Player", game: "Game") -> None:
        """
        Trigger turn ending effects.

        """
        for effect in self.turn_end_effects:
            effect.handler(player, game)

    def register_buy_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on buying.

        """
        self.buy_effects.append(effect)

    def unregister_buy_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on buying.

        """
        self._unregister_effects(name, self.buy_effects)

    def register_discard_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on discarding.

        """
        self.discard_effects.append(effect)

    def unregister_discard_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on discarding.

        """
        self._unregister_effects(name, self.discard_effects)

    def register_draw_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on drawing.

        """
        self.draw_effects.append(effect)

    def unregister_draw_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on drawing.

        """
        self._unregister_effects(name, self.draw_effects)

    def register_gain_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on gaining.

        """
        self.gain_effects.append(effect)

    def unregister_gain_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on gaining.

        """
        self._unregister_effects(name, self.gain_effects)

    def register_play_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on playing.

        """
        self.play_effects.append(effect)

    def unregister_play_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on playing.

        """
        self._unregister_effects(name, self.play_effects)

    def register_shuffle_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on shuffling.

        """
        self.shuffle_effects.append(effect)

    def unregister_shuffle_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on shuffling.

        """
        self._unregister_effects(name, self.shuffle_effects)

    def register_trash_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on trashing.

        """
        self.trash_effects.append(effect)

    def unregister_trash_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on trashing.

        """
        self._unregister_effects(name, self.trash_effects)

    def register_turn_start_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn starting.

        """
        self.turn_start_effects.append(effect)

    def unregister_turn_start_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on turn starting.

        """
        self._unregister_effects(name, self.turn_start_effects)

    def register_turn_end_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn ending.

        """
        self.turn_end_effects.append(effect)

    def unregister_turn_end_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on turn ending.

        """
        self._unregister_effects(name, self.turn_end_effects)
