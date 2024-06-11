from pyminion.expansions.base import throne_room
from pyminion.expansions.alchemy import alchemist, potion
from pyminion.game import Game
from pyminion.human import Human


def test_alchemist_topdeck(human: Human, game: Game, monkeypatch):
    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(alchemist)
    human.playmat.add(potion)

    human.play(alchemist, game)
    assert len(responses) == 1
    assert len(human.playmat) == 2
    assert set(card.name for card in human.playmat) == {"Alchemist", "Potion"}
    assert len(human.hand) == 2
    assert human.state.actions == 1

    human.start_cleanup_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 0
    discard_pile_names = set(card.name for card in human.discard_pile)
    assert "Potion" in discard_pile_names
    assert "Alchemist" not in discard_pile_names
    new_hand_names = set(card.name for card in human.hand)
    assert "Alchemist" in new_hand_names

    human.end_turn(game)


def test_alchemist_no_topdeck(human: Human, game: Game, monkeypatch):
    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(alchemist)
    human.playmat.add(potion)

    human.play(alchemist, game)
    assert len(responses) == 1
    assert len(human.playmat) == 2
    assert set(card.name for card in human.playmat) == {"Alchemist", "Potion"}
    assert len(human.hand) == 2
    assert human.state.actions == 1

    human.start_cleanup_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 0
    discard_pile_names = set(card.name for card in human.discard_pile)
    assert "Potion" in discard_pile_names
    assert "Alchemist" in discard_pile_names
    new_hand_names = set(card.name for card in human.hand)
    assert "Alchemist" not in new_hand_names


def test_alchemist_no_potion(human: Human, game: Game, monkeypatch):
    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(alchemist)

    human.play(alchemist, game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Alchemist"
    assert len(human.hand) == 2
    assert human.state.actions == 1

    human.start_cleanup_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 0
    discard_pile_names = set(card.name for card in human.discard_pile)
    assert "Alchemist" in discard_pile_names
    new_hand_names = set(card.name for card in human.hand)
    assert "Alchemist" not in new_hand_names


def test_alchemist_throne_room(human: Human, game: Game, monkeypatch):
    responses = ["alchemist", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(throne_room)
    human.hand.add(alchemist)
    human.playmat.add(potion)

    human.play(throne_room, game)
    assert len(responses) == 1
    assert len(human.playmat) == 3
    assert set(card.name for card in human.playmat) == {"Alchemist", "Potion", "Throne Room"}
    assert len(human.hand) == 4
    assert human.state.actions == 2

    human.start_cleanup_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 0
    discard_pile_names = set(card.name for card in human.discard_pile)
    assert "Potion" in discard_pile_names
    assert "Throne Room" in discard_pile_names
    assert "Alchemist" not in discard_pile_names
    new_hand_names = set(card.name for card in human.hand)
    assert "Alchemist" in new_hand_names

    human.end_turn(game)
