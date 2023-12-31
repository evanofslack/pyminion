from pyminion.core import Card
from pyminion.effects import Effect
from pyminion.expansions.base import gold, smithy
from pyminion.game import Game
from pyminion.player import Player


class HandlerTester:
    def __init__(self):
        self.handler_called = False

    def handler(self, player: Player, card: Card, game: Game) -> None:
        self.handler_called = True


def test_on_gain(game: Game):
    reg = game.effect_registry

    tester = HandlerTester()

    reg.register_on_gain_handler(Effect("test", tester.handler))

    player = game.players[0]
    player.hand.add(gold)
    player.hand.add(gold)
    player.play(gold, game)
    player.play(gold, game)

    player.buy(smithy, game)

    assert tester.handler_called
