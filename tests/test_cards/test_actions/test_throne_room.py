from pyminion.game import Game
from pyminion.models.base import smithy, throne_room, village
from pyminion.players import Human


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


# def test_vassal_no_play(human: Human, game: Game, monkeypatch):
#     human.deck.add(smithy)
#     human.hand.add(vassal)

#     monkeypatch.setattr("builtins.input", lambda _: "n")

#     human.hand.cards[0].play(human, game)
#     assert len(human.hand) == 0
#     assert len(human.playmat) == 1
#     assert len(human.discard_pile) == 1
#     assert human.state.actions == 0
#     assert human.state.money == 2
