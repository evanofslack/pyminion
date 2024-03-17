from pyminion.expansions.base import Smithy, smithy
from pyminion.expansions.intrigue import lurker
from pyminion.game import Game
from pyminion.human import Human
import pytest


@pytest.mark.kingdom_cards([smithy])
def test_lurker_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(lurker)
    assert len(human.hand) == 1
    assert len(human.playmat) == 0
    assert game.supply.pile_length(smithy.name) == 10
    assert len(game.trash) == 0

    responses = iter(["1", smithy.name])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(lurker, game)
    assert human.state.actions == 1
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert game.supply.pile_length(smithy.name) == 9
    assert len(game.trash) == 1


@pytest.mark.kingdom_cards([smithy])
def test_lurker_gain(human: Human, game: Game, monkeypatch):
    human.hand.add(lurker)
    game.trash.add(smithy)
    assert len(human.hand) == 1
    assert len(human.playmat) == 0
    assert len(game.trash) == 1

    responses = iter(["2", smithy.name])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(lurker, game)
    assert human.state.actions == 1
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(game.trash) == 0
    assert len(human.discard_pile.cards) == 1
    assert type(human.discard_pile.cards[-1]) is Smithy
