from typing import Optional

from pyminion.bots import OptimizedBot
from pyminion.expansions.base import copper, duchy, estate, gold, sentry, smithy
from pyminion.game import Game
from pyminion.players import Human


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


def test_sentry_bot_no_response(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(gold)
    bot.deck.add(smithy)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(bot.discard_pile) == 0
    assert len(game.trash) == 0
    assert bot.deck.cards[1].name == "Smithy"
    assert bot.deck.cards[0].name == "Gold"

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 0
    assert len(game.trash) == 0
    assert bot.state.actions == 1

    assert len(bot.deck) == 2
    assert bot.deck.cards[1].name == "Smithy"
    assert bot.deck.cards[0].name == "Gold"


def test_bot_trash_two(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(gold)
    bot.deck.add(copper)
    bot.deck.add(estate)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(game.trash) == 0

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 0
    assert len(game.trash) == 2
    assert len(bot.deck) == 1


def test_bot_discard_two(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(duchy)
    bot.deck.add(duchy)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(bot.discard_pile) == 0

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 2
    assert len(bot.deck) == 0


def test_bot_discard_one_trash_one(bot: OptimizedBot, game: Game):
    bot.deck.cards = []
    bot.deck.add(duchy)
    bot.deck.add(estate)
    bot.deck.add(copper)
    bot.hand.add(sentry)
    assert len(game.trash) == 0
    assert len(bot.discard_pile) == 0

    bot.play(sentry, game)
    assert len(bot.hand) == 1
    assert len(bot.playmat) == 1
    assert len(bot.discard_pile) == 1
    assert len(game.trash) == 1
    assert len(bot.deck) == 0
