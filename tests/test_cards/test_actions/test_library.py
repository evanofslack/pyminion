from pyminion.expansions.base import copper, library, smithy
from pyminion.game import Game
from pyminion.human import Human


def test_library_draw_7(human: Human, game: Game):
    human.hand.add(library)
    human.play(library, game)
    assert len(human.hand) == 7
    assert len(human.playmat) == 1
    assert human.state.actions == 0


def test_library_skip_action(human: Human, game: Game, monkeypatch):
    human.deck.add(smithy)
    human.hand.add(library)
    assert len(human.discard_pile) == 0

    monkeypatch.setattr("builtins.input", lambda _: "yes")

    human.play(library, game)
    assert len(human.hand) == 7
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Smithy"


def test_library_skip_action_small_deck(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.deck.add(copper)
    human.deck.add(copper)
    human.deck.add(smithy)

    human.hand.add(library)
    assert len(human.discard_pile) == 0

    monkeypatch.setattr("builtins.input", lambda _: "yes")

    human.play(library, game)
    assert len(human.hand) == 2
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Smithy"


def test_library_keep_action(human: Human, game: Game, monkeypatch):
    human.deck.add(smithy)
    human.hand.add(library)
    assert len(human.discard_pile) == 0

    monkeypatch.setattr("builtins.input", lambda _: "no")

    human.play(library, game)
    assert len(human.hand) == 7
    assert len(human.discard_pile) == 0
