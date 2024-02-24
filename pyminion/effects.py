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


class AttackEffect:
    def __init__(self, name: str):
        self.name = name

    def handler(self, attacking_player: "Player", defending_player: "Player", attack_card: "Card", game: "Game") -> bool:
        raise NotImplementedError("AttackEffect handler is not implemented")


class EffectRegistry:
    """
    Registry for effects to be triggered on various game events.

    """
    def __init__(self):
        self.attack_effects: List[AttackEffect] = []
        self.buy_effects: List[PlayerCardGameEffect] = []
        self.discard_effects: List[PlayerCardGameEffect] = []
        self.draw_effects: List[PlayerCardGameEffect] = []
        self.gain_effects: List[PlayerCardGameEffect] = []
        self.play_effects: List[PlayerCardGameEffect] = []
        self.reveal_effects: List[PlayerCardGameEffect] = []
        self.shuffle_effects: List[PlayerGameEffect] = []
        self.trash_effects: List[PlayerCardGameEffect] = []
        self.turn_start_effects: List[PlayerGameEffect] = []
        self.turn_end_effects: List[PlayerGameEffect] = []
        self.cleanup_start_effects: List[PlayerGameEffect] = []

    def _unregister_effects(self, name: str, effect_list: Union[List[PlayerGameEffect], List[PlayerCardGameEffect], List[AttackEffect]]) -> None:
        i = 0
        while i < len(effect_list):
            effect = effect_list[i]
            if effect.name == name:
                effect_list.pop(i)
            else:
                i += 1

    def on_attack(self, attacking_player: "Player", defending_player: "Player", attack_card: "Card", game: "Game") -> bool:
        """
        Trigger attacking effects.

        """
        attacked = True
        for effect in self.attack_effects:
            attacked &= effect.handler(attacking_player, defending_player, attack_card, game)
        return attacked

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

    def on_reveal(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger revealing effects.

        """
        for effect in self.reveal_effects:
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
        Trigger turn start effects.

        """
        for effect in self.turn_start_effects:
            effect.handler(player, game)

    def on_turn_end(self, player: "Player", game: "Game") -> None:
        """
        Trigger turn end effects.

        """
        for effect in self.turn_end_effects:
            effect.handler(player, game)

    def on_cleanup_start(self, player: "Player", game: "Game") -> None:
        """
        Trigger clean-up start effects.

        """
        for effect in self.cleanup_start_effects:
            effect.handler(player, game)

    def register_attack_effect(self, effect: AttackEffect) -> None:
        """
        Register an effect to be triggered on attacking.

        """
        self.attack_effects.append(effect)

    def unregister_attack_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on attacking.

        """
        self._unregister_effects(name, self.attack_effects)

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

    def register_reveal_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on revealing.

        """
        self.reveal_effects.append(effect)

    def unregister_reveal_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on revealing.

        """
        self._unregister_effects(name, self.reveal_effects)

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
        Register an effect to be triggered on turn start.

        """
        self.turn_start_effects.append(effect)

    def unregister_turn_start_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on turn start.

        """
        self._unregister_effects(name, self.turn_start_effects)

    def register_turn_end_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn end.

        """
        self.turn_end_effects.append(effect)

    def unregister_turn_end_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on turn end.

        """
        self._unregister_effects(name, self.turn_end_effects)

    def register_cleanup_start_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on clean-up start.

        """
        self.cleanup_start_effects.append(effect)

    def unregister_cleanup_start_effects(self, name: str) -> None:
        """
        Unregister an effect from being triggered on clean-up start.

        """
        self._unregister_effects(name, self.cleanup_start_effects)
