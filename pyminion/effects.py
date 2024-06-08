from enum import IntEnum, unique
from typing import TYPE_CHECKING, Callable, Sequence

if TYPE_CHECKING:
    from pyminion.core import AbstractDeck, Card
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
    First = 4
    Last = 5


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
        is_triggered_func: PlayerGameEffectTriggerHandler | None = None,
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
        raise NotImplementedError(
            "PlayerCardGameEffect is_triggered is not implemented"
        )

    def handler(self, player: "Player", card: "Card", game: "Game") -> None:
        raise NotImplementedError("PlayerCardGameEffect handler is not implemented")


class FuncPlayerCardGameEffect(PlayerCardGameEffect):
    def __init__(
        self,
        name: str,
        action: EffectAction,
        handler_func: PlayerCardGameEffectHandler,
        is_triggered_func: PlayerCardGameEffectTriggerHandler | None = None,
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


class PlayerCardGameDeckEffect(Effect):
    def __init__(self, name: str):
        super().__init__(name)

    def is_triggered(self, player: "Player", card: "Card", game: "Game", destination: "AbstractDeck") -> bool:
        raise NotImplementedError("PlayerCardGameDeckEffect is_triggered is not implemented")

    def handler(self, player: "Player", card: "Card", game: "Game", destination: "AbstractDeck") -> None:
        raise NotImplementedError("PlayerCardGameDeckEffect handler is not implemented")


class AttackEffect(Effect):
    def __init__(self, name: str, action: EffectAction):
        super().__init__(name)
        self._action = action

    def get_action(self) -> EffectAction:
        return self._action

    def is_triggered(
        self,
        attacking_player: "Player",
        defending_player: "Player",
        attack_card: "Card",
        game: "Game",
    ) -> bool:
        raise NotImplementedError("AttackEffect handler is not implemented")

    def handler(
        self,
        attacking_player: "Player",
        defending_player: "Player",
        attack_card: "Card",
        game: "Game",
    ) -> bool:
        raise NotImplementedError("AttackEffect handler is not implemented")


class EffectRegistry:
    """
    Registry for effects to be triggered on various game events.

    """

    def __init__(self):
        self.attack_effects: list[AttackEffect] = []
        self.buy_effects: list[PlayerCardGameDeckEffect] = []
        self.discard_effects: list[PlayerCardGameDeckEffect] = []
        self.gain_effects: list[PlayerCardGameDeckEffect] = []
        self.hand_add_effects: list[PlayerCardGameEffect] = []
        self.hand_remove_effects: list[PlayerCardGameEffect] = []
        self.play_effects: list[PlayerCardGameEffect] = []
        self.reveal_effects: list[PlayerCardGameEffect] = []
        self.shuffle_effects: list[PlayerGameEffect] = []
        self.trash_effects: list[PlayerCardGameEffect] = []
        self.turn_start_effects: list[PlayerGameEffect] = []
        self.turn_end_effects: list[PlayerGameEffect] = []
        self.buy_phase_end_effects: list[PlayerGameEffect] = []
        self.cleanup_phase_start_effects: list[PlayerGameEffect] = []

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
        self.buy_phase_end_effects.clear()
        self.cleanup_phase_start_effects.clear()

    def _need_player_order(self, effects: Sequence[Effect]) -> bool:
        # if there is only one effect left, no need to prompt player
        if len(effects) == 1:
            return False

        grouped_effects: dict[EffectAction, list[Effect]] = {}
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
        effects: list[PlayerGameEffect],
        player: "Player",
        game: "Game",
    ) -> None:
        if len(effects) == 0:
            return

        handled_ids: set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, game))
        while not effect_ids.issubset(handled_ids):
            handled_effect = False

            # handle effects that happen before others
            for effect in effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.First and effect.is_triggered(player, game):
                    effect.handler(player, game)
                    handled_ids.add(effect.get_id())
                    handled_effect = True
                    break

            # handle all effects where order doesn't matter
            if not handled_effect:
                for effect in effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(player, game):
                        effect.handler(player, game)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_effect:
                # build data structures of non-"other" effects that are triggered
                order_effects: list[PlayerGameEffect] = [
                    effect for effect in effects
                    if effect.get_id() not in handled_ids and effect.get_action() in {EffectAction.HandAddCards, EffectAction.HandRemoveCards, EffectAction.HandAddRemoveCards} and effect.is_triggered(player, game)
                ]

                if len(order_effects) > 0:
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
                    handled_effect = True

            # handle effects that happen after others
            if not handled_effect:
                for effect in effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Last and effect.is_triggered(player, game):
                        effect.handler(player, game)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, game))

    def _handle_player_card_game_effects(
        self,
        effects: list[PlayerCardGameEffect],
        player: "Player",
        card: "Card",
        game: "Game",
    ) -> None:
        if len(effects) == 0:
            return

        handled_ids: set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, card, game))
        while not effect_ids.issubset(handled_ids):
            handled_effect = False

            # handle effects that happen before others
            for effect in effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.First and effect.is_triggered(player, card, game):
                    effect.handler(player, card, game)
                    handled_ids.add(effect.get_id())
                    handled_effect = True
                    break

            # handle all effects where order doesn't matter
            if not handled_effect:
                for effect in effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(player, card, game):
                        effect.handler(player, card, game)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_effect:
                # build data structures of non-"other" effects that are triggered
                order_effects: list[PlayerCardGameEffect] = [
                    effect for effect in effects
                    if effect.get_id() not in handled_ids and effect.get_action() in {EffectAction.HandAddCards, EffectAction.HandRemoveCards, EffectAction.HandAddRemoveCards} and effect.is_triggered(player, card, game)
                ]

                if len(order_effects) > 0:
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
                    handled_effect = True

            # handle effects that happen after others
            if not handled_effect:
                for effect in effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Last and effect.is_triggered(player, card, game):
                        effect.handler(player, card, game)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, card, game))

    def _handle_player_card_game_deck_effects(
        self,
        effects: list[PlayerCardGameDeckEffect],
        player: "Player",
        card: "Card",
        game: "Game",
        deck: "AbstractDeck",
    ) -> None:
        if len(effects) == 0:
            return

        handled_ids: set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, card, game, deck))
        while not effect_ids.issubset(handled_ids):
            handled_effect = False

            # handle effects that happen before others
            for effect in effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.First and effect.is_triggered(player, card, game, deck):
                    effect.handler(player, card, game, deck)
                    handled_ids.add(effect.get_id())
                    handled_effect = True
                    break

            # handle all effects where order doesn't matter
            if not handled_effect:
                for effect in effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(player, card, game, deck):
                        effect.handler(player, card, game, deck)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_effect:
                # build data structures of non-"other" effects that are triggered
                order_effects: list[PlayerCardGameDeckEffect] = [
                    effect for effect in effects
                    if effect.get_id() not in handled_ids and effect.get_action() in {EffectAction.HandAddCards, EffectAction.HandRemoveCards, EffectAction.HandAddRemoveCards} and effect.is_triggered(player, card, game, deck)
                ]

                if len(order_effects) > 0:
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
                    effect.handler(player, card, game, deck)
                    handled_ids.add(effect.get_id())
                    handled_effect = True

            # handle effects that happen after others
            if not handled_effect:
                for effect in effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Last and effect.is_triggered(player, card, game, deck):
                        effect.handler(player, card, game, deck)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in effects if e.is_triggered(player, card, game, deck))

    def _unregister_effect_by_id(
            self,
            id: int,
            effect_list: list[PlayerGameEffect]|list[PlayerCardGameEffect]|list[PlayerCardGameDeckEffect]|list[AttackEffect],
    ) -> None:
        i = 0
        while i < len(effect_list):
            effect = effect_list[i]
            if effect.get_id() == id:
                effect_list.pop(i)
                return
            i += 1

    def on_attack(self, attacking_player: "Player", defending_player: "Player", attack_card: "Card", game: "Game") -> bool:
        """
        Trigger attacking effects.

        """
        if len(self.attack_effects) == 0:
            return True

        attacked = True

        handled_ids: set[int] = set()

        # one effect may change others, so after handling each effect we need to
        # reevaluate which other effects need to be handled
        effect_ids = set(e.get_id() for e in self.attack_effects if e.is_triggered(attacking_player, defending_player, attack_card, game))
        while not effect_ids.issubset(handled_ids):
            handled_effect = False

            # handle effects that happen before others
            for effect in self.attack_effects:
                if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.First and effect.is_triggered(attacking_player, defending_player, attack_card, game):
                    attacked &= effect.handler(attacking_player, defending_player, attack_card, game)
                    handled_ids.add(effect.get_id())
                    handled_effect = True
                    break

            # handle all effects where order doesn't matter
            if not handled_effect:
                for effect in self.attack_effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Other and effect.is_triggered(attacking_player, defending_player, attack_card, game):
                        attacked &= effect.handler(attacking_player, defending_player, attack_card, game)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # if there were no "other" effects to handle, check if there were non-"other" effects
            if not handled_effect:
                # build data structures of non-"other" effects that are triggered
                order_effects: list[AttackEffect] = [
                    effect for effect in self.attack_effects
                    if effect.get_id() not in handled_ids and effect.get_action() in {EffectAction.HandAddCards, EffectAction.HandRemoveCards, EffectAction.HandAddRemoveCards} and effect.is_triggered(attacking_player, defending_player, attack_card, game)
                ]

                if len(order_effects) > 0:
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
                    handled_effect = True

            # handle effects that happen after others
            if not handled_effect:
                for effect in self.attack_effects:
                    if effect.get_id() not in handled_ids and effect.get_action() == EffectAction.Last and effect.is_triggered(attacking_player, defending_player, attack_card, game):
                        attacked &= effect.handler(attacking_player, defending_player, attack_card, game)
                        handled_ids.add(effect.get_id())
                        handled_effect = True
                        break

            # reevaluate which effects need to be handled
            effect_ids = set(e.get_id() for e in self.attack_effects if e.is_triggered(attacking_player, defending_player, attack_card, game))

        return attacked

    def on_buy(self, player: "Player", card: "Card", game: "Game", deck: "AbstractDeck") -> None:
        """
        Trigger buying effects.

        """
        self._handle_player_card_game_deck_effects(self.gain_effects + self.buy_effects, player, card, game, deck)

    def on_discard(self, player: "Player", card: "Card", game: "Game", deck: "AbstractDeck") -> None:
        """
        Trigger discarding effects.

        """
        self._handle_player_card_game_deck_effects(self.discard_effects, player, card, game, deck)

    def on_gain(self, player: "Player", card: "Card", game: "Game", deck: "AbstractDeck") -> None:
        """
        Trigger gaining effects.

        """
        self._handle_player_card_game_deck_effects(self.gain_effects, player, card, game, deck)

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

    def on_buy_phase_end(self, player: "Player", game: "Game") -> None:
        """
        Trigger buy phase end effects.

        """
        self._handle_player_game_effects(self.buy_phase_end_effects, player, game)

    def on_cleanup_phase_start(self, player: "Player", game: "Game") -> None:
        """
        Trigger clean-up phase start effects.

        """
        self._handle_player_game_effects(self.cleanup_phase_start_effects, player, game)

    def register_attack_effect(self, effect: AttackEffect) -> None:
        """
        Register an effect to be triggered on attacking.

        """
        self.attack_effects.append(effect)

    def unregister_attack_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on attacking.

        """
        self._unregister_effect_by_id(id, self.attack_effects)

    def register_buy_effect(self, effect: PlayerCardGameDeckEffect) -> None:
        """
        Register an effect to be triggered on buying.

        """
        self.buy_effects.append(effect)

    def unregister_buy_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on buying.

        """
        self._unregister_effect_by_id(id, self.buy_effects)

    def register_discard_effect(self, effect: PlayerCardGameDeckEffect) -> None:
        """
        Register an effect to be triggered on discarding.

        """
        self.discard_effects.append(effect)

    def unregister_discard_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on discarding.

        """
        self._unregister_effect_by_id(id, self.discard_effects)

    def register_gain_effect(self, effect: PlayerCardGameDeckEffect) -> None:
        """
        Register an effect to be triggered on gaining.

        """
        self.gain_effects.append(effect)

    def unregister_gain_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on gaining.

        """
        self._unregister_effect_by_id(id, self.gain_effects)

    def register_hand_add_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on hand adding.

        """
        self.hand_add_effects.append(effect)

    def unregister_hand_add_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on hand adding.

        """
        self._unregister_effect_by_id(id, self.hand_add_effects)

    def register_hand_remove_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on hand removing.

        """
        self.hand_remove_effects.append(effect)

    def unregister_hand_remove_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on hand removing.

        """
        self._unregister_effect_by_id(id, self.hand_remove_effects)

    def register_play_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on playing.

        """
        self.play_effects.append(effect)

    def unregister_play_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on playing.

        """
        self._unregister_effect_by_id(id, self.play_effects)

    def register_reveal_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on revealing.

        """
        self.reveal_effects.append(effect)

    def unregister_reveal_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on revealing.

        """
        self._unregister_effect_by_id(id, self.reveal_effects)

    def register_shuffle_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on shuffling.

        """
        self.shuffle_effects.append(effect)

    def unregister_shuffle_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on shuffling.

        """
        self._unregister_effect_by_id(id, self.shuffle_effects)

    def register_trash_effect(self, effect: PlayerCardGameEffect) -> None:
        """
        Register an effect to be triggered on trashing.

        """
        self.trash_effects.append(effect)

    def unregister_trash_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on trashing.

        """
        self._unregister_effect_by_id(id, self.trash_effects)

    def register_turn_start_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn start.

        """
        self.turn_start_effects.append(effect)

    def unregister_turn_start_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on turn start.

        """
        self._unregister_effect_by_id(id, self.turn_start_effects)

    def register_turn_end_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on turn end.

        """
        self.turn_end_effects.append(effect)

    def unregister_turn_end_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on turn end.

        """
        self._unregister_effect_by_id(id, self.turn_end_effects)

    def register_buy_phase_end_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on buy phase end.

        """
        self.buy_phase_end_effects.append(effect)

    def unregister_buy_phase_end_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on buy phase end.

        """
        self._unregister_effect_by_id(id, self.buy_phase_end_effects)

    def register_cleanup_phase_start_effect(self, effect: PlayerGameEffect) -> None:
        """
        Register an effect to be triggered on clean-up phase start.

        """
        self.cleanup_phase_start_effects.append(effect)

    def unregister_cleanup_phase_start_effect(self, id: int) -> None:
        """
        Unregister an effect from being triggered on clean-up phase start.

        """
        self._unregister_effect_by_id(id, self.cleanup_phase_start_effects)
