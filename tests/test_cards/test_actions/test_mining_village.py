from pyminion.core import DeckCounter
from pyminion.expansions.base import ThroneRoom, throne_room
from pyminion.expansions.intrigue import MiningVillage, mining_village
from pyminion.game import Game
from pyminion.human import Human


def test_mining_village_no_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(mining_village)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    human.play(mining_village, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is MiningVillage
    assert len(game.trash) == 0
    assert human.state.actions == 2
    assert human.state.money == 0


def test_mining_village_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(mining_village)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(mining_village, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 0
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is MiningVillage
    assert human.state.actions == 2
    assert human.state.money == 2


def test_mining_village_throne_room_no_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(mining_village)

    responses = iter(["Mining Village", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(throne_room, game)
    assert len(human.hand) == 2
    counter = DeckCounter(human.playmat.cards)
    assert sum(counter.values()) == 2
    assert counter[throne_room] == 1
    assert counter[mining_village] == 1
    assert len(game.trash) == 0
    assert human.state.actions == 4
    assert human.state.money == 0


def test_mining_village_throne_room_trash_1st(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(mining_village)

    # if Mining Village is trashed the first time it is played, it cannot be
    # trashed again because it is already in the trash
    responses = iter(["Mining Village", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(throne_room, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is ThroneRoom
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is MiningVillage
    assert human.state.actions == 4
    assert human.state.money == 2


def test_mining_village_throne_room_trash_2nd(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(mining_village)

    responses = iter(["Mining Village", "n", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(throne_room, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is ThroneRoom
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is MiningVillage
    assert human.state.actions == 4
    assert human.state.money == 2
