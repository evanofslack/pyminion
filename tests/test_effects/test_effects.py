from pyminion.core import Card
from pyminion.effects import EffectOrderType, EffectRegistry, AttackEffect, PlayerCardGameEffect, PlayerGameEffect
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
        order: EffectOrderType = EffectOrderType.Hidden,
        order_counter: Optional[OrderCounter] = None,
    ):
        super().__init__(name, order)
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
            order: EffectOrderType = EffectOrderType.Hidden,
            order_counter: Optional[OrderCounter] = None,
    ):
        super().__init__(name)
        self._order = order
        self.handler_called = False
        self.order_counter = order_counter
        self.order_count = -1

    def get_order(self) -> EffectOrderType:
        return self._order

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
        order: EffectOrderType = EffectOrderType.Hidden,
        order_counter: Optional[OrderCounter] = None,
    ):
        super().__init__(name)
        self._order = order
        self.handler_called = False
        self.order_counter = order_counter
        self.order_count = -1

    def get_order(self) -> EffectOrderType:
        return self._order

    def is_triggered(self, player: Player, game: Game) -> bool:
        return True

    def handler(self, player: Player, game: Game) -> None:
        self.handler_called = True
        if self.order_counter is not None:
            self.order_count = self.order_counter.inc_count()


def test_register_effects(effect_registry: EffectRegistry):
    assert len(effect_registry.attack_effects) == 0
    assert len(effect_registry.buy_effects) == 0
    assert len(effect_registry.discard_effects) == 0
    assert len(effect_registry.gain_effects) == 0
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


def test_attack_effect_order(multiplayer_game: Game, monkeypatch):
    reg = multiplayer_game.effect_registry
    order_counter = OrderCounter()

    hidden_effect = AttackEffectTest("Hidden", EffectOrderType.Hidden, order_counter)
    order_not_required_effect = AttackEffectTest("OrderNotRequired", EffectOrderType.OrderNotRequired, order_counter)
    order_required_effect1 = AttackEffectTest("OrderRequired1", EffectOrderType.OrderRequired, order_counter)
    order_required_effect2 = AttackEffectTest("OrderRequired2", EffectOrderType.OrderRequired, order_counter)

    reg.register_attack_effect(order_required_effect1)
    reg.register_attack_effect(order_required_effect2)
    reg.register_attack_effect(order_not_required_effect)
    reg.register_attack_effect(hidden_effect)

    responses = iter(["2, 3, 1"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    player = multiplayer_game.players[0]
    player.hand.add(witch)
    player.play(witch, multiplayer_game)

    assert hidden_effect.order_count == 0
    assert order_required_effect2.order_count == 1
    assert order_not_required_effect.order_count == 2
    assert order_required_effect1.order_count == 3


def test_player_card_game_effect_order(multiplayer_game: Game, monkeypatch):
    reg = multiplayer_game.effect_registry
    order_counter = OrderCounter()

    hidden_effect = PlayerCardGameEffectTest("Hidden", EffectOrderType.Hidden, order_counter)
    order_not_required_effect = PlayerCardGameEffectTest("OrderNotRequired", EffectOrderType.OrderNotRequired, order_counter)
    order_required_effect1 = PlayerCardGameEffectTest("OrderRequired1", EffectOrderType.OrderRequired, order_counter)
    order_required_effect2 = PlayerCardGameEffectTest("OrderRequired2", EffectOrderType.OrderRequired, order_counter)

    reg.register_gain_effect(order_required_effect1)
    reg.register_gain_effect(order_required_effect2)
    reg.register_gain_effect(order_not_required_effect)
    reg.register_gain_effect(hidden_effect)

    responses = iter(["2, 3, 1"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    player = multiplayer_game.players[0]
    player.gain(gold, multiplayer_game)

    assert hidden_effect.order_count == 0
    assert order_required_effect2.order_count == 1
    assert order_not_required_effect.order_count == 2
    assert order_required_effect1.order_count == 3


def test_player_game_effect_order(multiplayer_game: Game, monkeypatch):
    reg = multiplayer_game.effect_registry
    order_counter = OrderCounter()

    hidden_effect = PlayerGameEffectTest("Hidden", EffectOrderType.Hidden, order_counter)
    order_not_required_effect = PlayerGameEffectTest("OrderNotRequired", EffectOrderType.OrderNotRequired, order_counter)
    order_required_effect1 = PlayerGameEffectTest("OrderRequired1", EffectOrderType.OrderRequired, order_counter)
    order_required_effect2 = PlayerGameEffectTest("OrderRequired2", EffectOrderType.OrderRequired, order_counter)

    reg.register_shuffle_effect(order_required_effect1)
    reg.register_shuffle_effect(order_required_effect2)
    reg.register_shuffle_effect(order_not_required_effect)
    reg.register_shuffle_effect(hidden_effect)

    responses = iter(["2, 3, 1"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    player = multiplayer_game.players[0]
    player.deck.move_to(player.discard_pile)
    player.draw() # trigger shuffle

    assert hidden_effect.order_count == 0
    assert order_required_effect2.order_count == 1
    assert order_not_required_effect.order_count == 2
    assert order_required_effect1.order_count == 3


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
