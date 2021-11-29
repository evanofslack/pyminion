from pyminion.bots import OptimizedBot
from pyminion.expansions.base import copper, gold, sentry
from pyminion.game import Game
from pyminion.players import Human


def test_sentry_no_response(human: Human, game: Game, monkeypatch):
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
