from pyminion.expansions.base import copper, estate
from pyminion.expansions.intrigue import intrigue_set, conspirator, nobles
from pyminion.expansions.alchemy import alchemy_set, transmute
from pyminion.game import Game
from pyminion.human import Human
import pytest


@pytest.mark.expansions([intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([transmute, conspirator])
def test_transmute_action(human: Human, game: Game, monkeypatch):
    human.hand.add(transmute)
    human.hand.add(conspirator)
    human.hand.add(copper)

    responses = ["Conspirator"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(transmute, game)
    assert len(responses) == 0
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Duchy"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Conspirator"


@pytest.mark.expansions([intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([transmute])
def test_transmute_treasure(human: Human, game: Game, monkeypatch):
    human.hand.add(transmute)
    human.hand.add(estate)
    human.hand.add(copper)

    responses = ["Copper"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(transmute, game)
    assert len(responses) == 0
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Transmute"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Copper"


@pytest.mark.expansions([intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([transmute])
def test_transmute_victory(human: Human, game: Game, monkeypatch):
    human.hand.add(transmute)
    human.hand.add(estate)
    human.hand.add(copper)

    responses = ["Estate"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(transmute, game)
    assert len(responses) == 0
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Gold"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Estate"


@pytest.mark.expansions([intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([transmute])
def test_transmute_empty_hand(human: Human, game: Game, monkeypatch):
    human.hand.add(transmute)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(transmute, game)
    assert len(responses) == 0
    assert len(human.hand) == 0
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0


@pytest.mark.expansions([intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([transmute])
def test_transmute_one_card_hand(human: Human, game: Game, monkeypatch):
    human.hand.add(transmute)
    human.hand.add(copper)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(transmute, game)
    assert len(responses) == 0
    assert len(human.hand) == 0
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Transmute"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Copper"


@pytest.mark.expansions([intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([transmute])
def test_transmute_multi_type_card(human: Human, game: Game, monkeypatch):
    human.hand.add(transmute)
    human.hand.add(nobles)
    human.hand.add(copper)

    responses = ["Nobles"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(transmute, game)
    assert len(responses) == 0
    assert len(human.hand) == 1
    assert len(human.discard_pile) == 2
    assert human.discard_pile.cards[0].name == "Duchy"
    assert human.discard_pile.cards[1].name == "Gold"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Nobles"
