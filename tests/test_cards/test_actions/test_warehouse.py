from pyminion.expansions.base import curse, estate, duchy, silver
from pyminion.expansions.seaside import warehouse
from pyminion.game import Game
from pyminion.human import Human


def test_warehouse_many_cards(human: Human, game: Game, monkeypatch):
    human.deck.add(silver)
    human.deck.add(curse)
    human.deck.add(estate)

    human.hand.add(duchy)
    human.hand.add(warehouse)

    responses = ["curse, estate, duchy"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(warehouse, game)
    assert len(responses) == 0
    assert human.state.actions == 1
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Warehouse"
    assert len(human.hand) == 1
    assert human.hand.cards[0].name == "Silver"
    assert len(human.discard_pile) == 3
    assert set(c.name for c in human.discard_pile) == {"Curse", "Estate", "Duchy"}


def test_warehouse_few_cards(human: Human, game: Game, monkeypatch):
    human.deck.cards = []

    human.deck.add(silver)

    human.hand.add(duchy)
    human.hand.add(warehouse)

    human.play(warehouse, game)
    assert human.state.actions == 1
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Warehouse"
    assert len(human.hand) == 0
    assert len(human.discard_pile) == 2
    assert set(c.name for c in human.discard_pile) == {"Silver", "Duchy"}
