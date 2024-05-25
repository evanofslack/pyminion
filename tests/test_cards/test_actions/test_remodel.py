from pyminion.expansions.base import copper, remodel
from pyminion.expansions.alchemy import alchemy_set, apothecary, golem
from pyminion.game import Game
from pyminion.human import Human
import pytest


def test_remodel_gain_valid(human: Human, game: Game, monkeypatch):
    human.hand.add(copper)
    human.hand.add(copper)
    human.hand.add(remodel)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0

    responses = iter(["copper", "estate"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(remodel, game)
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.discard_pile.cards[0].name == "Estate"
    assert game.trash.cards[0].name == "Copper"


def test_remodel_1_card_hand(human: Human, game: Game, monkeypatch):
    human.hand.add(copper)
    human.hand.add(remodel)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0

    responses = iter(["estate"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(remodel, game)
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.discard_pile.cards[0].name == "Estate"
    assert game.trash.cards[0].name == "Copper"


def test_remodel_empty_hand(human: Human, game: Game):
    human.hand.add(remodel)
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0

    human.play(remodel, game)
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0
    assert human.state.actions == 0


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([apothecary, golem])
def test_remodel_potion_cost(human: Human, game: Game, monkeypatch):
    human.hand.add(apothecary)
    human.hand.add(copper)
    human.hand.add(remodel)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0

    responses = ["apothecary", "golem"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(remodel, game)
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.discard_pile.cards[0].name == "Golem"
    assert game.trash.cards[0].name == "Apothecary"
