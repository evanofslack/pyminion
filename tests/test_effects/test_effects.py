from pyminion.core import Card
from pyminion.effects import EffectRegistry, AttackEffect, PlayerCardGameEffect, PlayerGameEffect
from pyminion.expansions.base import gold, smithy, witch
from pyminion.game import Game
from pyminion.player import Player
import pytest


class AttackEffectTest(AttackEffect):
    def __init__(self, name: str = "AttackEffectTest"):
        super().__init__(name)
        self.handler_called = False

    def handler(self, attacking_player: Player, defending_player: Player, attack_card: Card, game: Game) -> bool:
        self.handler_called = True
        return True


class PlayerCardGameEffectTest(PlayerCardGameEffect):
    def __init__(self, name: str = "PlayerCardGameEffectTest"):
        super().__init__(name)
        self.handler_called = False

    def handler(self, player: Player, card: Card, game: Game) -> None:
        self.handler_called = True


class PlayerGameEffectTest(PlayerGameEffect):
    def __init__(self, name: str = "PlayerGameEffectTest"):
        super().__init__(name)
        self.handler_called = False

    def handler(self, player: Player, game: Game) -> None:
        self.handler_called = True


def test_register_effects(effect_registry: EffectRegistry):
    assert len(effect_registry.attack_effects) == 0
    assert len(effect_registry.buy_effects) == 0
    assert len(effect_registry.discard_effects) == 0
    assert len(effect_registry.draw_effects) == 0
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
    effect_registry.register_draw_effect(PlayerCardGameEffectTest())
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
    assert len(effect_registry.draw_effects) == 1
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
    assert len(effect_registry.draw_effects) == 0
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
    effect_registry.register_draw_effect(PlayerCardGameEffectTest())
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
    assert len(effect_registry.draw_effects) == 1
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
    effect_registry.unregister_draw_effects("PlayerCardGameEffectTest")
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
    assert len(effect_registry.draw_effects) == 0
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


def test_on_draw(game: Game):
    reg = game.effect_registry

    draw_effect = PlayerCardGameEffectTest()
    reg.register_draw_effect(draw_effect)

    player = game.players[0]
    player.draw(game)

    assert draw_effect.handler_called


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
