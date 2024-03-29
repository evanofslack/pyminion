from enum import IntEnum, unique
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Sequence, Set, Union

if TYPE_CHECKING:
    from pyminion.core import Card
    from pyminion.game import Game
    from pyminion.player import Player


PlayerGameEffectHandler = Callable[["Player", "Game"], None]
PlayerGameEffectTriggerHandler = Callable[["Player", "Game"], bool]
PlayerCardGameEffectHandler = Callable[["Player", "Card", "Game"], None]
PlayerCardGameEffectTriggerHandler = Callable[["Player", "Card", "Game"], bool]


@unique
class EffectAction(IntEnum):
    Other = 0
    HandAddCards = 1
    HandRemoveCards = 2
    HandAddRemoveCards = 3


class Effect:
    _next_id = 0

    @staticmethod
    def reset_id() -> None:
        Effect._next_id = 0

    def __init__(self, name: str):
        self._id = Effect._next_id
        Effect._next_id += 1
        self._name = name

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_action(self) -> EffectAction:
        raise NotImplementedError("Effect get_action is not implemented")


class PlayerGameEffect(Effect):
    def __init__(self, name: str):
        super().__init__(name)

    def is_triggered(self, player: "Player", game: "Game") -> bool:
        raise NotImplementedError("PlayerGameEffect is_triggered is not implemented")

    def handler(self, player: "Player", game: "Game") -> None:
        raise NotImplementedError("PlayerGameEffect handler is not implemented")


class FuncPlayerGameEffect(PlayerGameEffect):
    def __init__(
        self,
        name: str,
        action: EffectAction,
        handler_func: PlayerGameEffectHandler,
        is_triggered_func: Optional[PlayerGameEffectTriggerHandler] = None,
    ):
        super().__init__(name)
        self._action = action
        self.handler_func = handler_func

        self.is_triggered_func: PlayerGameEffectTriggerHandler
        if is_triggered_func is None:
            self.is_triggered_func = lambda p, g: True
        else:
            self.is_triggered_func = is_triggered_func

    def get_action(self) -> EffectAction:
        return self._action

    def is_triggered(self, player: "Player", game: "Game") -> bool:
        return self.is_triggered_func(player, game)

    def handler(self, player: "Player", game: "Game") -> None:
        self.handler_func(player, game)


class PlayerCardGameEffect(Effect):
    def __init__(self, name: str):
        super().__init__(name)

    def is_triggered(self, player: "Player", card: "Card", game: "Game") -> bool:
        raise NotImplementedError("PlayerCardGameEffect is_triggered is not implemented")

    def handler(self, player: "Player", card: "Card", game: "Game") -> None:
        raise NotImplementedError("PlayerCardGameEffect handler is not implemented")


class FuncPlayerCardGameEffect(PlayerCardGameEffect):
    def __init__(
        self,
        name: str,
        action: EffectAction,
        handler_func: PlayerCardGameEffectHandler,
        is_triggered_func: Optional[PlayerCardGameEffectTriggerHandler] = None,
    ):
        super().__init__(name)
        self._action = action
        self.handler_func = handler_func

        self.is_triggered_func: PlayerCardGameEffectTriggerHandler
        if is_triggered_func is None:
            self.is_triggered_func = lambda p, c, g: True
        else:
            self.is_triggered_func = is_triggered_func

    def get_action(self) -> EffectAction:
        return self._action

    def is_triggered(self, player: "Player", card: "Card", game: "Game") -> bool:
        return self.is_triggered_func(player, card, game)

    def handler(self, player: "Player", card: "Card", game: "Game") -> None:
        self.handler_func(player, card, game)


class AttackEffect(Effect):
    def __init__(self, name: str, action: EffectAction):
        super().__init__(name)
        self._action = action

    def get_action(self) -> EffectAction:
        return self._action

    def is_triggered(self, attacking_player: "Player", defending_player: "Player", attack_card: "Card", game: "Game") -> bool:
        raise NotImplementedError("AttackEffect handler is not implemented")

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
        self.gain_effects: List[PlayerCardGameEffect] = []
        self.hand_add_effects: List[PlayerCardGameEffect] = []
        self.hand_remove_effects: List[PlayerCardGameEffect] = []
        self.play_effects: List[PlayerCardGameEffect] = []
        self.reveal_effects: List[PlayerCardGameEffect] = []
        self.shuffle_effects: List[PlayerGameEffect] = []
        self.trash_effects: List[PlayerCardGameEffect] = []
        self.turn_start_effects: List[PlayerGameEffect] = []
        self.turn_end_effects: List[PlayerGameEffect] = []
        self.cleanup_start_effects: List[PlayerGameEffect] = []

    def reset(self) -> None:
        """
        Reset the registry for a new game.

        """
        Effect.reset_id()

        self.attack_effects.clear()
        self.buy_effects.clear()
        self.discard_effects.clear()
        self.gain_effects.clear()
        self.hand_add_effects.clear()
        self.hand_remove_effects.clear()
        self.play_effects.clear()
        self.reveal_effects.clear()
        self.shuffle_effects.clear()
        self.trash_effects.clear()
        self.turn_start_effects.clear()
        self.turn_end_effects.clear()
        self.cleanup_start_effects.clear()

    def _need_player_order(self, effects: Sequence[Effect]) -> bool:
        # if there is only one effect left, no need to prompt player
        if len(effects) == 1:
            return False

        grouped_effects: Dict[EffectAction, List[Effect]] = {}
        for effect in effects:
            action = effect.get_action()
            if action in grouped_effects:
                grouped_effects[action].append(effect)
            else:
                grouped_effects[action] = [effect]

        if len(grouped_effects) > 1:
            return True

        if EffectAction.HandAddRemoveCards in grouped_effects:
            unique_names = set(grouped_effects[EffectAction.HandAddRemoveCards])
            if len(unique_names) > 1:
                return True

        return False

    def _handle_player_game_effects(
            self,
            effects: List[PlayerGameEffect],
            player: "Player",
            game: "Game",
    ) -> None:
        if len(effects) == 0:
            return

        handled_ids: Set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, game))
        while not effect_ids.issubset(handled_ids):
            # handle all effects where order doesn't matter
            handled_other = False
            for effect in effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(player, game):
                    effect.handler(player, game)
                    handled_ids.add(effect.get_id())
                    handled_other = True
                    break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_other:
                # build data structures of non-"other" effects that are triggered
                order_effects: List[PlayerGameEffect] = [
                    effect for effect in effects
                    if effect.get_id() not in handled_ids and effect.get_action() != EffectAction.Other and effect.is_triggered(player, game)
                ]

                # if there were no more effects to handle we should have exited the loop by now
                assert len(order_effects) > 0

                if self._need_player_order(order_effects):
                    # ask user to specify next effect to execute
                    effect_index = player.decider.effects_order_decision(
                        order_effects,
                        player,
                        game,
                    )
                else:
                    effect_index = 0

                effect = order_effects[effect_index]
                effect.handler(player, game)
                handled_ids.add(effect.get_id())

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, game))

    def _handle_player_card_game_effects(
            self,
            effects: List[PlayerCardGameEffect],
            player: "Player",
            card: "Card",
            game: "Game",
    ) -> None:
        if len(effects) == 0:
            return

        handled_ids: Set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, card, game))
        while not effect_ids.issubset(handled_ids):
            # handle all effects where order doesn't matter
            handled_other = False
            for effect in effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(player, card, game):
                    effect.handler(player, card, game)
                    handled_ids.add(effect.get_id())
                    handled_other = True
                    break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_other:
                # build data structures of non-"other" effects that are triggered
                order_effects: List[PlayerCardGameEffect] = [
                    effect for effect in effects
                    if effect.get_id() not in handled_ids and effect.get_action() != EffectAction.Other and effect.is_triggered(player, card, game)
                ]

                # if there were no more effects to handle we should have exited the loop by now
                assert len(order_effects) > 0

                if self._need_player_order(order_effects):
                    # ask user to specify next effect to execute
                    effect_index = player.decider.effects_order_decision(
                        order_effects,
                        player,
                        game,
                    )
                else:
                    effect_index = 0

                effect = order_effects[effect_index]
                effect.handler(player, card, game)
                handled_ids.add(effect.get_id())

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, card, game))

    def _unregister_effects(
            self,
            name: str,
            effect_list: Union[List[PlayerGameEffect], List[PlayerCardGameEffect], List[AttackEffect]],
            max_unregister: int,
    ) -> None:
        unregister_count = 0
        i = 0
        while i < len(effect_list) and (max_unregister < 0 or unregister_count < max_unregister):
            effect = effect_list[i]
            if effect.get_name() == name:
                effect_list.pop(i)
                unregister_count += 1
            else:
                i += 1

    def on_attack(self, attacking_player: "Player", defending_player: "Player", attack_card: "Card", game: "Game") -> bool:
        """
        Trigger attacking effects.

        """
        if len(self.attack_effects) == 0:
            return True

        attacked = True

        handled_ids: Set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in self.attack_effects if e.is_triggered(attacking_player, defending_player, attack_card, game))
        while not effect_ids.issubset(handled_ids):
            # handle all effects where order doesn't matter
            handled_other = False
            for effect in self.attack_effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(attacking_player, defending_player, attack_card, game):
                    attacked &= effect.handler(attacking_player, defending_player, attack_card, game)
                    handled_ids.add(effect.get_id())
                    handled_other = True
                    break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_other:
                # build data structures of non-"other" effects that are triggered
                order_effects: List[AttackEffect] = [
                    effect for effect in self.attack_effects
                    if effect.get_id() not in handled_ids and effect.get_action() != EffectAction.Other and effect.is_triggered(attacking_player, defending_player, attack_card, game)
                ]

                # if there were no more effects to handle we should have exited the loop by now
                assert len(order_effects) > 0

                if self._need_player_order(order_effects):
                    # ask user to specify next effect to execute
                    effect_index = defending_player.decider.effects_order_decision(
                        order_effects,
                        defending_player,
                        game,
                    )
                else:
                    effect_index = 0

                effect = order_effects[effect_index]
                attacked &= effect.handler(attacking_player, defending_player, attack_card, game)
                handled_ids.add(effect.get_id())

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in self.attack_effects if e.is_triggered(attacking_player, defending_player, attack_card, game))

        return attacked

    def on_buy(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger buying effects.

        """
        self._handle_player_card_game_effects(self.gain_effects + self.buy_effects, player, card, game)

    def on_discard(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger discarding effects.

        """
        self._handle_player_card_game_effects(self.discard_effects, player, card, game)

    def on_gain(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger gaining effects.

        """
        self._handle_player_card_game_effects(self.gain_effects, player, card, game)

    def on_hand_add(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger hand adding effects.

        """
        self._handle_player_card_game_effects(self.hand_add_effects, player, card, game)

    def on_hand_remove(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger hand removing effects.

        """
        self._handle_player_card_game_effects(self.hand_remove_effects, player, card, game)

    def on_play(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger playing effects.

        """
        self._handle_player_card_game_effects(self.play_effects, player, card, game)

    def on_reveal(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger revealing effects.

        """
        self._handle_player_card_game_effects(self.reveal_effects, player, card, game)

    def on_shuffle(self, player: "Player", game: "Game") -> None:
        """
        Trigger shuffling effects.

        """
        self._handle_player_game_effects(self.shuffle_effects, player, game)

    def on_trash(self, player: "Player", card: "Card", game: "Game") -> None:
        """
        Trigger trashing effects.

        """
        self._handle_player_card_game_effects(self.trash_effects, player, card, game)

    def on_turn_start(self, player: "Player", game: "Game") -> None:
        """
        Trigger turn start effects.

        """
        self._handle_player_game_effects(self.turn_start_effects, player, game)

    def on_turn_end(self, player: "Player", game: "Game") -> None:
        """
        Trigger turn end effects.

        """
        self._handle_player_game_effects(self.turn_end_effects, player, game)

    def on_cleanup_start(self, player: "Player", game: "Game") -> None:
        """
        Trigger clean-up start effects.

        """
        self._handle_player_game_effects(self.cleanup_start_effects, player, game)

    def register_attack_effect(self, effect: AttackEffect) -> None:
        """
        Register an effect to be triggered on attacking.

        """
        self.attack_effects.append(effect)

    def unregister_attack_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on attacking.

        """
        self._unregister_effects(name, self.attack_effects, max_unregister)

    def register_buy_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on buying.

        """
        self.buy_effects.append(effect)

    def unregister_buy_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on buying.

        """
        self._unregister_effects(name, self.buy_effects, max_unregister)

    def register_discard_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on discarding.

        """
        self.discard_effects.append(effect)

    def unregister_discard_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on discarding.

        """
        self._unregister_effects(name, self.discard_effects, max_unregister)

    def register_gain_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on gaining.

        """
        self.gain_effects.append(effect)

    def unregister_gain_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on gaining.

        """
        self._unregister_effects(name, self.gain_effects, max_unregister)

    def register_hand_add_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on hand adding.

        """
        self.hand_add_effects.append(effect)

    def unregister_hand_add_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on hand adding.

        """
        self._unregister_effects(name, self.hand_add_effects, max_unregister)

    def register_hand_remove_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on hand removing.

        """
        self.hand_remove_effects.append(effect)

    def unregister_hand_remove_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on hand removing.

        """
        self._unregister_effects(name, self.hand_remove_effects, max_unregister)

    def register_play_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on playing.

        """
        self.play_effects.append(effect)

    def unregister_play_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on playing.

        """
        self._unregister_effects(name, self.play_effects, max_unregister)

    def register_reveal_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on revealing.

        """
        self.reveal_effects.append(effect)

    def unregister_reveal_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on revealing.

        """
        self._unregister_effects(name, self.reveal_effects, max_unregister)

    def register_shuffle_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on shuffling.

        """
        self.shuffle_effects.append(effect)

    def unregister_shuffle_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on shuffling.

        """
        self._unregister_effects(name, self.shuffle_effects, max_unregister)

    def register_trash_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on trashing.

        """
        self.trash_effects.append(effect)

    def unregister_trash_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on trashing.

        """
        self._unregister_effects(name, self.trash_effects, max_unregister)

    def register_turn_start_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn start.

        """
        self.turn_start_effects.append(effect)

    def unregister_turn_start_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on turn start.

        """
        self._unregister_effects(name, self.turn_start_effects, max_unregister)

    def register_turn_end_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn end.

        """
        self.turn_end_effects.append(effect)

    def unregister_turn_end_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on turn end.

        """
        self._unregister_effects(name, self.turn_end_effects, max_unregister)

    def register_cleanup_start_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on clean-up start.

        """
        self.cleanup_start_effects.append(effect)

    def unregister_cleanup_start_effects(self, name: str, max_unregister: int = -1) -> None:
        """
        Unregister an effect from being triggered on clean-up start.

        """
        self._unregister_effects(name, self.cleanup_start_effects, max_unregister)
