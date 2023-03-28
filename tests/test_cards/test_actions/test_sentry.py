from pyminion.expansions.base import copper, estate, gold, sentry
from pyminion.game import Game
from pyminion.human import Human


def test_sentry_no_reorder(human: Human, game: Game, monkeypatch):
    human.deck.cards = []
    human.deck.add(gold)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(sentry)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.deck.cards[1].name == "Copper"
    assert human.deck.cards[0].name == "Gold"

    responses = iter(["", "", "no"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(sentry, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.state.actions == 1

    assert len(human.deck) == 2
    assert human.deck.cards[1].name == "Copper"
    assert human.deck.cards[0].name == "Gold"


def test_sentry_yes_reorder(human: Human, game: Game, monkeypatch):
    human.deck.cards = []
    human.deck.add(gold)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(sentry)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.deck.cards[1].name == "Copper"
    assert human.deck.cards[0].name == "Gold"

    responses = iter(["", "", "yes"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(sentry, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.state.actions == 1

    assert len(human.deck) == 2
    assert human.deck.cards[0].name == "Copper"
    assert human.deck.cards[1].name == "Gold"


def test_sentry_trash_two(human: Human, game: Game, monkeypatch):
    human.deck.cards = []
    human.deck.add(estate)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(sentry)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.deck.cards[1].name == "Copper"
    assert human.deck.cards[0].name == "Estate"

    responses = iter(["copper, estate"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(sentry, game)
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 2

    assert len(human.deck) == 0


def test_sentry_discard_two(human: Human, game: Game, monkeypatch):
    human.deck.cards = []
    human.deck.add(estate)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(sentry)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.deck.cards[1].name == "Copper"
    assert human.deck.cards[0].name == "Estate"

    responses = iter(["", "copper, estate"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(sentry, game)
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 2
    assert len(game.trash) == 0

    assert len(human.deck) == 0


def test_sentry_trash_one_discard_one(human: Human, game: Game, monkeypatch):
    human.deck.cards = []
    human.deck.add(estate)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(sentry)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.deck.cards[1].name == "Copper"
    assert human.deck.cards[0].name == "Estate"

    responses = iter(["copper", "estate"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(sentry, game)
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 1
    assert len(game.trash) == 1

    assert len(human.deck) == 0
