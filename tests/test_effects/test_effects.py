from pyminion.core import Card
from pyminion.effects import Effect, EffectAction, EffectRegistry, AttackEffect, PlayerCardGameEffect, PlayerGameEffect
from pyminion.expansions.base import gold, smithy, witch
from pyminion.game import Game
from pyminion.player import Player
import pytest
from typing import Optional


class OrderCounter:
    def __init__(self):
        self._count = 0

    def inc_count(self) -> int:
        ret = self._count
        self._count += 1
        return ret


class AttackEffectTest(AttackEffect):
    def __init__(
        self,
        name: str = "AttackEffectTest",
        action: EffectAction = EffectAction.Other,
        order_counter: Optional[OrderCounter] = None,
    ):
        super().__init__(name, action)
        self.handler_called = False
        self.order_counter = order_counter
        self.order_count = -1

    def is_triggered(self, attacking_player: Player, defending_player: Player, attack_card: Card, game: "Game") -> bool:
        return True

    def handler(self, attacking_player: Player, defending_player: Player, attack_card: Card, game: Game) -> bool:
        self.handler_called = True
        if self.order_counter is not None:
            self.order_count = self.order_counter.inc_count()
        return True


class PlayerCardGameEffectTest(PlayerCardGameEffect):
    def __init__(
            self,
            name: str = "PlayerCardGameEffectTest",
            action: EffectAction = EffectAction.Other,
            order_counter: Optional[OrderCounter] = None,
    ):
        super().__init__(name)
        self._action = action
        self.handler_called = False
        self.order_counter = order_counter
        self.order_count = -1

    def get_action(self) -> EffectAction:
        return self._action

    def is_triggered(self, player: Player, card: Card, game: Game) -> bool:
        return True

    def handler(self, player: Player, card: Card, game: Game) -> None:
        self.handler_called = True
        if self.order_counter is not None:
            self.order_count = self.order_counter.inc_count()


class PlayerGameEffectTest(PlayerGameEffect):
    def __init__(
        self,
        name: str = "PlayerGameEffectTest",
        action: EffectAction = EffectAction.Other,
        order_counter: Optional[OrderCounter] = None,
    ):
        super().__init__(name)
        self._action = action
        self.handler_called = False
        self.order_counter = order_counter
        self.order_count = -1

    def get_action(self) -> EffectAction:
        return self._action

    def is_triggered(self, player: Player, game: Game) -> bool:
        return True

    def handler(self, player: Player, game: Game) -> None:
        self.handler_called = True
        if self.order_counter is not None:
            self.order_count = self.order_counter.inc_count()


def test_effect_id():
    e1 = Effect("e1")
    e2 = Effect("e2")
    e3 = Effect("e3")
    assert e1.get_id() != e2.get_id() != e3.get_id()


def test_register_effects(effect_registry: EffectRegistry):
    assert len(effect_registry.attack_effects) == 0
    assert len(effect_registry.buy_effects) == 0
    assert len(effect_registry.discard_effects) == 0
    assert len(effect_registry.gain_effects) == 0
    assert len(effect_registry.hand_add_effects) == 0
    assert len(effect_registry.hand_remove_effects) == 0
    assert len(effect_registry.play_effects) == 0
    assert len(effect_registry.reveal_effects) == 0
    assert len(effect_registry.shuffle_effects) == 0
    assert len(effect_registry.trash_effects) == 0
    assert len(effect_registry.turn_start_effects) == 0
    assert len(effect_registry.turn_end_effects) == 0
    assert len(effect_registry.cleanup_start_effects) == 0

    effect_registry.register_attack_effect(AttackEffectTest())
    effect_registry.register_buy_effect(PlayerCardGameEffectTest())
    effect_registry.register_discard_effect(PlayerCardGameEffectTest())
    effect_registry.register_gain_effect(PlayerCardGameEffectTest())
    effect_registry.register_hand_add_effect(PlayerCardGameEffectTest())
    effect_registry.register_hand_remove_effect(PlayerCardGameEffectTest())
    effect_registry.register_play_effect(PlayerCardGameEffectTest())
    effect_registry.register_reveal_effect(PlayerCardGameEffectTest())
    effect_registry.register_shuffle_effect(PlayerGameEffectTest())
    effect_registry.register_trash_effect(PlayerCardGameEffectTest())
    effect_registry.register_turn_start_effect(PlayerGameEffectTest())
    effect_registry.register_turn_end_effect(PlayerGameEffectTest())
    effect_registry.register_cleanup_start_effect(PlayerGameEffectTest())

    assert len(effect_registry.attack_effects) == 1
    assert len(effect_registry.buy_effects) == 1
    assert len(effect_registry.discard_effects) == 1
    assert len(effect_registry.gain_effects) == 1
    assert len(effect_registry.hand_add_effects) == 1
    assert len(effect_registry.hand_remove_effects) == 1
    assert len(effect_registry.play_effects) == 1
    assert len(effect_registry.reveal_effects) == 1
    assert len(effect_registry.shuffle_effects) == 1
    assert len(effect_registry.trash_effects) == 1
    assert len(effect_registry.turn_start_effects) == 1
    assert len(effect_registry.turn_end_effects) == 1
    assert len(effect_registry.cleanup_start_effects) == 1


def test_unregister_effects(effect_registry: EffectRegistry):
    assert len(effect_registry.attack_effects) == 0
    assert len(effect_registry.buy_effects) == 0
    assert len(effect_registry.discard_effects) == 0
    assert len(effect_registry.gain_effects) == 0
    assert len(effect_registry.hand_add_effects) == 0
    assert len(effect_registry.hand_remove_effects) == 0
    assert len(effect_registry.play_effects) == 0
    assert len(effect_registry.reveal_effects) == 0
    assert len(effect_registry.shuffle_effects) == 0
    assert len(effect_registry.trash_effects) == 0
    assert len(effect_registry.turn_start_effects) == 0
    assert len(effect_registry.turn_end_effects) == 0
    assert len(effect_registry.cleanup_start_effects) == 0

    effect_registry.register_attack_effect(AttackEffectTest())
    effect_registry.register_buy_effect(PlayerCardGameEffectTest())
    effect_registry.register_discard_effect(PlayerCardGameEffectTest())
    effect_registry.register_gain_effect(PlayerCardGameEffectTest())
    effect_registry.register_hand_add_effect(PlayerCardGameEffectTest())
    effect_registry.register_hand_remove_effect(PlayerCardGameEffectTest())
    effect_registry.register_play_effect(PlayerCardGameEffectTest())
    effect_registry.register_reveal_effect(PlayerCardGameEffectTest())
    effect_registry.register_shuffle_effect(PlayerGameEffectTest())
    effect_registry.register_trash_effect(PlayerCardGameEffectTest())
    effect_registry.register_turn_start_effect(PlayerGameEffectTest())
    effect_registry.register_turn_end_effect(PlayerGameEffectTest())
    effect_registry.register_cleanup_start_effect(PlayerGameEffectTest())

    assert len(effect_registry.attack_effects) == 1
    assert len(effect_registry.buy_effects) == 1
    assert len(effect_registry.discard_effects) == 1
    assert len(effect_registry.gain_effects) == 1
    assert len(effect_registry.hand_add_effects) == 1
    assert len(effect_registry.hand_remove_effects) == 1
    assert len(effect_registry.play_effects) == 1
    assert len(effect_registry.reveal_effects) == 1
    assert len(effect_registry.shuffle_effects) == 1
    assert len(effect_registry.trash_effects) == 1
    assert len(effect_registry.turn_start_effects) == 1
    assert len(effect_registry.turn_end_effects) == 1
    assert len(effect_registry.cleanup_start_effects) == 1

    effect_registry.unregister_attack_effects("AttackEffectTest")
    effect_registry.unregister_buy_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_discard_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_gain_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_hand_add_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_hand_remove_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_play_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_reveal_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_shuffle_effects("PlayerGameEffectTest")
    effect_registry.unregister_trash_effects("PlayerCardGameEffectTest")
    effect_registry.unregister_turn_start_effects("PlayerGameEffectTest")
    effect_registry.unregister_turn_end_effects("PlayerGameEffectTest")
    effect_registry.unregister_cleanup_start_effects("PlayerGameEffectTest")

    assert len(effect_registry.attack_effects) == 0
    assert len(effect_registry.buy_effects) == 0
    assert len(effect_registry.discard_effects) == 0
    assert len(effect_registry.gain_effects) == 0
    assert len(effect_registry.hand_add_effects) == 0
    assert len(effect_registry.hand_remove_effects) == 0
    assert len(effect_registry.play_effects) == 0
    assert len(effect_registry.reveal_effects) == 0
    assert len(effect_registry.shuffle_effects) == 0
    assert len(effect_registry.trash_effects) == 0
    assert len(effect_registry.turn_start_effects) == 0
    assert len(effect_registry.turn_end_effects) == 0
    assert len(effect_registry.cleanup_start_effects) == 0


def test_register_unregister_multiple_effects(effect_registry: EffectRegistry):
    assert len(effect_registry.attack_effects) == 0

    effect_registry.register_attack_effect(AttackEffectTest("test1"))
    effect_registry.register_attack_effect(AttackEffectTest("test1"))
    effect_registry.register_attack_effect(AttackEffectTest("test2"))

    assert len(effect_registry.attack_effects) == 3

    effect_registry.unregister_attack_effects("test1")

    assert len(effect_registry.attack_effects) == 1

    effect_registry.register_attack_effect(AttackEffectTest("test1"))
    effect_registry.register_attack_effect(AttackEffectTest("test1"))

    assert len(effect_registry.attack_effects) == 3

    effect_registry.unregister_attack_effects("test1", max_unregister=1)

    assert len(effect_registry.attack_effects) == 2


def test_order_player_card_game_other(multiplayer_game: Game):
    order_counter = OrderCounter()
    effect_registry = multiplayer_game.effect_registry
    player = multiplayer_game.players[0]

    e1 = PlayerCardGameEffectTest("e1", EffectAction.Other, order_counter)
    effect_registry.register_reveal_effect(e1)

    e2 = PlayerCardGameEffectTest("e2", EffectAction.Other, order_counter)
    effect_registry.register_reveal_effect(e2)

    player.reveal(player.hand.cards[0], multiplayer_game)

    assert e1.order_count == 0
    assert e2.order_count == 1


def test_order_player_card_game_other_hand_add(multiplayer_game: Game):
    order_counter = OrderCounter()
    effect_registry = multiplayer_game.effect_registry
    player = multiplayer_game.players[0]

    e1 = PlayerCardGameEffectTest("e1", EffectAction.HandAddCards, order_counter)
    effect_registry.register_reveal_effect(e1)

    e2 = PlayerCardGameEffectTest("e2", EffectAction.Other, order_counter)
    effect_registry.register_reveal_effect(e2)

    e3 = PlayerCardGameEffectTest("e3", EffectAction.HandAddCards, order_counter)
    effect_registry.register_reveal_effect(e3)

    player.reveal(player.hand.cards[0], multiplayer_game)

    assert e2.order_count == 0
    assert e1.order_count == 1
    assert e3.order_count == 2


def test_order_player_card_game_hand_add_hand_remove(multiplayer_game: Game, monkeypatch):
    order_counter = OrderCounter()
    effect_registry = multiplayer_game.effect_registry
    player = multiplayer_game.players[0]

    e1 = PlayerCardGameEffectTest("e1", EffectAction.HandAddCards, order_counter)
    effect_registry.register_reveal_effect(e1)

    e2 = PlayerCardGameEffectTest("e2", EffectAction.Other, order_counter)
    effect_registry.register_reveal_effect(e2)

    e3 = PlayerCardGameEffectTest("e3", EffectAction.HandRemoveCards, order_counter)
    effect_registry.register_reveal_effect(e3)

    responses = iter(["2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    player.reveal(player.hand.cards[0], multiplayer_game)

    assert e2.order_count == 0
    assert e3.order_count == 1
    assert e1.order_count == 2


def test_order_player_card_game_hand_add_remove(multiplayer_game: Game, monkeypatch):
    order_counter = OrderCounter()
    effect_registry = multiplayer_game.effect_registry
    player = multiplayer_game.players[0]

    e1 = PlayerCardGameEffectTest("e1", EffectAction.HandAddRemoveCards, order_counter)
    effect_registry.register_reveal_effect(e1)

    e2 = PlayerCardGameEffectTest("e2", EffectAction.Other, order_counter)
    effect_registry.register_reveal_effect(e2)

    e3 = PlayerCardGameEffectTest("e3", EffectAction.HandAddRemoveCards, order_counter)
    effect_registry.register_reveal_effect(e3)

    responses = iter(["2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    player.reveal(player.hand.cards[0], multiplayer_game)

    assert e2.order_count == 0
    assert e3.order_count == 1
    assert e1.order_count == 2


@pytest.mark.kingdom_cards([witch])
def test_on_attack(multiplayer_game: Game):
    reg = multiplayer_game.effect_registry

    attack_effect = AttackEffectTest()
    reg.register_attack_effect(attack_effect)

    player = multiplayer_game.players[0]
    player.hand.add(witch)
    player.play(witch, multiplayer_game)

    assert attack_effect.handler_called


@pytest.mark.kingdom_cards([smithy])
def test_on_buy(game: Game):
    reg = game.effect_registry

    buy_effect = PlayerCardGameEffectTest()
    gain_effect = PlayerCardGameEffectTest()
    reg.register_buy_effect(buy_effect)
    reg.register_gain_effect(gain_effect)

    player = game.players[0]
    player.hand.add(gold)
    player.hand.add(gold)
    player.play(gold, game)
    player.play(gold, game)

    player.buy(smithy, game)

    assert buy_effect.handler_called
    assert gain_effect.handler_called


def test_on_discard(game: Game):
    reg = game.effect_registry

    discard_effect = PlayerCardGameEffectTest()
    reg.register_discard_effect(discard_effect)

    player = game.players[0]
    player.hand.add(gold)
    player.discard(game, player.hand.cards[0])

    assert discard_effect.handler_called


@pytest.mark.kingdom_cards([smithy])
def test_on_gain(game: Game):
    reg = game.effect_registry

    buy_effect = PlayerCardGameEffectTest()
    gain_effect = PlayerCardGameEffectTest()
    reg.register_buy_effect(buy_effect)
    reg.register_gain_effect(gain_effect)

    player = game.players[0]
    player.gain(smithy, game)

    assert not buy_effect.handler_called
    assert gain_effect.handler_called
