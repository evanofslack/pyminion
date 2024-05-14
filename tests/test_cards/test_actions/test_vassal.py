from pyminion.expansions.base import estate, smithy, vassal, village
from pyminion.game import Game
from pyminion.human import Human


def test_vassal_not_action_play(human: Human, game: Game):
    human.hand.add(vassal)

    human.play(vassal, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.state.money == 2


def test_vassal_no_play(human: Human, game: Game, monkeypatch):
    human.deck.add(smithy)
    human.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    human.play(vassal, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.state.money == 2


def test_vassal_play(human: Human, game: Game, monkeypatch):
    human.deck.add(smithy)
    human.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(vassal, game)
    assert len(human.hand) == 3
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.money == 2


def test_vassal_play_chain_two(human: Human, game: Game, monkeypatch):
    human.deck.add(vassal)
    human.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(vassal, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 1
    assert (human.discard_pile.cards[-1]) == estate
    assert human.state.actions == 0
    assert human.state.money == 4


def test_vassal_play_chain_three(human: Human, game: Game, monkeypatch):
    human.deck.add(vassal)
    human.deck.add(vassal)
    human.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(vassal, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 3
    assert len(human.discard_pile) == 1
    assert (human.discard_pile.cards[-1]) == estate
    assert human.state.actions == 0
    assert human.state.money == 6


def test_vassal_play_chain_smithy(human: Human, game: Game, monkeypatch):
    human.deck.add(smithy)
    human.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(vassal, game)
    assert len(human.hand) == 3
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.money == 2


def test_vassal_play_chain_village(human: Human, game: Game, monkeypatch):
    human.deck.add(village)
    human.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(vassal, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 0
    assert human.state.actions == 2
    assert human.state.money == 2


def test_vassal_no_cards(human: Human, game: Game):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()
    human.hand.add(vassal)

    human.play(vassal, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(human.deck) == 0
    assert len(human.discard_pile) == 0
    assert human.state.actions == 0
    assert human.state.money == 2
