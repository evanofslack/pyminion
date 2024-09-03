from pyminion.expansions.base import (
    base_set,
    artisan,
    cellar,
    copper,
    festival,
    market,
    moat,
    smithy,
    vassal,
    village,
    witch,
)
from pyminion.expansions.intrigue import Swindler, intrigue_set, swindler
from pyminion.expansions.alchemy import alchemy_set, familiar, philosophers_stone
from pyminion.game import Game
import pytest


def test_swindler(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(swindler)
    p2.deck.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "curse")

    p1.play(swindler, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Swindler
    assert p1.state.actions == 0
    assert p1.state.money == 2

    assert len(p2.discard_pile) > 0
    assert p2.discard_pile.cards[-1].name == "Curse"

    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Copper"


@pytest.mark.kingdom_cards([moat])
def test_swindler_moat(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(swindler)
    p2.deck.add(moat)
    p2.deck.add(moat)
    p2.draw()

    monkeypatch.setattr("builtins.input", lambda _: "y")

    p1.play(swindler, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Swindler
    assert p1.state.actions == 0
    assert p1.state.money == 2

    assert p2.deck.cards[-1].name == "Moat"
    assert len(p2.discard_pile) == 0

    assert len(multiplayer_game.trash) == 0


# create a kingdom with only one $4 cost card (smithy)
@pytest.mark.expansions([base_set, intrigue_set])
@pytest.mark.kingdom_cards([artisan, cellar, festival, market, moat, smithy, swindler, vassal, village, witch])
def test_swindler_no_gain(multiplayer_game: Game, monkeypatch):
    # empty smithy pile
    multiplayer_game.supply.get_pile("Smithy").cards.clear()

    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(swindler)
    p2.deck.add(smithy)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1.play(swindler, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Swindler
    assert p1.state.actions == 0
    assert p1.state.money == 2

    assert len(p2.discard_pile) == 0

    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Smithy"


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([familiar, philosophers_stone])
def test_swindler_potion_cost(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.hand.add(swindler)
    p2.deck.add(familiar)

    responses = ["Philosopher's Stone"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1.play(swindler, multiplayer_game)
    assert len(p1.hand) == 5
    assert len(p1.playmat) == 1
    assert type(p1.playmat.cards[0]) is Swindler
    assert p1.state.actions == 0
    assert p1.state.money == 2

    assert len(p2.discard_pile) > 0
    assert p2.discard_pile.cards[-1].name == "Philosopher's Stone"

    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Familiar"
