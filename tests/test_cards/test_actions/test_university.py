from pyminion.expansions.base import (
    base_set,
    council_room,
    gardens,
    artisan,
)
from pyminion.expansions.intrigue import (
    intrigue_set,
    farm,
    nobles,
)
from pyminion.expansions.alchemy import (
    alchemy_set,
    apothecary,
    familiar,
    scrying_pool,
    transmute,
    university,
    vineyard,
)
from pyminion.game import Game
from pyminion.human import Human
import pytest


@pytest.mark.expansions([base_set])
@pytest.mark.kingdom_cards([council_room])
def test_university_gain(human: Human, game: Game, monkeypatch):
    human.hand.add(university)

    responses = ["y", "council room"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(university, game)
    assert len(responses) == 0
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Council Room"
    assert human.state.actions == 2


@pytest.mark.expansions([base_set])
@pytest.mark.kingdom_cards([council_room])
def test_university_no_gain(human: Human, game: Game, monkeypatch):
    human.hand.add(university)

    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(university, game)
    assert len(responses) == 0
    assert len(human.discard_pile) == 0
    assert human.state.actions == 2


# kingdom with no action cards with cost $5 or less
@pytest.mark.expansions([base_set, intrigue_set, alchemy_set])
@pytest.mark.kingdom_cards([
    artisan,
    gardens,
    farm,
    nobles,
    apothecary,
    familiar,
    scrying_pool,
    transmute,
    university,
    vineyard,
])
def test_university_no_valid_cards(human: Human, game: Game, monkeypatch):
    human.hand.add(university)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(university, game)
    assert len(responses) == 0
    assert len(human.discard_pile) == 0
    assert human.state.actions == 2
