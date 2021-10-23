from pyminion.models.core import Player, Turn, Game
from pyminion.expansions.base import copper, smithy
from pyminion.exceptions import InsufficientActions

import pytest


def test_create_turn(player: Player):
    turn = Turn(player=player)
    assert turn.actions == 1
    assert turn.money == 0
    assert turn.buys == 1


def test_play_treasure_increment_money(player: Player, turn: Turn):
    player.hand.add(copper)
    assert turn.money == 0
    player.hand.cards[0].play(turn, player)
    assert turn.money == 1


def test_play_action_decrement_action(player: Player, turn: Turn, game: Game):
    player.hand.add(smithy)
    assert turn.actions == 1
    player.hand.cards[0].play(turn, player, game)
    assert turn.actions == 0


def test_insufficents_actions(player: Player, turn: Turn, game: Game):
    player.hand.add(smithy)
    player.hand.add(smithy)
    player.hand.cards[0].play(turn, player, game)
    assert turn.actions == 0
    with pytest.raises(InsufficientActions):
        player.hand.cards[0].play(turn, player, game)
