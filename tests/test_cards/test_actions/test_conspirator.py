from pyminion.expansions.base import throne_room
from pyminion.expansions.intrigue import conspirator, shanty_town
from pyminion.human import Human
from pyminion.player import Player
from pyminion.game import Game


def test_conspirator_1_action(player: Player, game: Game):
    player.hand.add(conspirator)

    player.play(conspirator, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert player.actions_played_this_turn == 1
    assert player.state.actions == 0
    assert player.state.money == 2


def test_conspirator_multiple_actions(player: Player, game: Game):
    player.hand.add(shanty_town)
    player.hand.add(conspirator)
    player.hand.add(conspirator)
    player.hand.add(conspirator)

    player.play(shanty_town, game)
    player.play(conspirator, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 2
    assert player.actions_played_this_turn == 2
    assert player.state.actions == 1
    assert player.state.money == 2

    player.play(conspirator, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 3
    assert player.actions_played_this_turn == 3
    assert player.state.actions == 1
    assert player.state.money == 4

    player.play(conspirator, game)
    assert len(player.hand) == 2
    assert len(player.playmat) == 4
    assert player.actions_played_this_turn == 4
    assert player.state.actions == 1
    assert player.state.money == 6


def test_conspirator_throne_room(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(conspirator)

    monkeypatch.setattr("builtins.input", lambda _: "conspirator")

    human.play(throne_room, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 2
    assert human.actions_played_this_turn == 3
    assert human.state.actions == 1
    assert human.state.money == 4
