from pyminion.expansions.base import smithy, throne_room, village
from pyminion.game import Game
from pyminion.human import Human


def test_throne_room_no_action(human: Human, game: Game):
    human.hand.add(throne_room)

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.money == 0


def test_throne_room_smithy(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(smithy)
    assert len(human.hand) == 2

    monkeypatch.setattr("builtins.input", lambda _: "Smithy")

    human.hand.cards[0].play(human, game)
    assert len(human.playmat) == 2
    assert len(human.hand) == 6

    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.money == 0


def test_throne_room_village(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(village)
    assert len(human.hand) == 2
    assert human.state.actions == 1

    monkeypatch.setattr("builtins.input", lambda _: "Village")

    human.hand.cards[0].play(human, game)
    assert len(human.playmat) == 2
    assert len(human.hand) == 2
    assert human.state.actions == 4

    assert human.state.money == 0


def test_two_separate_thrones(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(village)
    assert len(human.hand) == 2
    assert human.state.actions == 1

    monkeypatch.setattr("builtins.input", lambda _: "Village")

    human.hand.cards[0].play(human, game)
    assert len(human.playmat) == 2
    assert len(human.hand) == 2
    assert human.state.actions == 4

    human.hand.add(throne_room)
    human.hand.add(smithy)

    assert len(human.hand) == 4

    monkeypatch.setattr("builtins.input", lambda _: "Smithy")
    human.play(throne_room, game=game)
    assert len(human.playmat) == 4
    assert len(human.hand) == 8
    assert human.state.actions == 3

    assert human.state.money == 0


def test_throne_a_throne(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(throne_room)
    human.hand.add(smithy)
    human.hand.add(smithy)
    assert len(human.hand) == 4

    for i in range(20):
        human.deck.add(throne_room)

    responses = iter(["throne room", "smithy", "smithy"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(target_card=throne_room, game=game)

    assert len(human.playmat) == 4
    assert len(human.hand) == 12  # +3 cards played 4 times = 12 cards
