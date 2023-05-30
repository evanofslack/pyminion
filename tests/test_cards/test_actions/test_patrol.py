from pyminion.core import DeckCounter
from pyminion.expansions.base import copper, silver, gold, estate, curse
from pyminion.expansions.intrigue import Patrol, patrol
from pyminion.game import Game
from pyminion.human import Human


def test_patrol(human: Human, game: Game, monkeypatch):
    human.deck.add(silver)
    human.deck.add(gold)
    human.deck.add(estate)
    human.deck.add(curse)
    human.deck.add(copper)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(patrol)

    monkeypatch.setattr("builtins.input", lambda _: "silver, gold")

    human.play(patrol, game)
    counter = DeckCounter(human.hand.cards)
    assert sum(counter.values()) == 5
    assert counter[copper] == 3
    assert counter[estate] == 1
    assert counter[curse] == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Patrol
    assert len(human.deck) >= 2
    assert human.deck.cards[-1].name == "Gold"
    assert human.deck.cards[-2].name == "Silver"


def test_patrol_1_topdeck(human: Human, game: Game, monkeypatch):
    human.deck.add(silver)
    human.deck.add(estate)
    human.deck.add(estate)
    human.deck.add(curse)
    human.deck.add(copper)
    human.deck.add(copper)
    human.deck.add(copper)
    human.hand.add(patrol)

    human.play(patrol, game)
    counter = DeckCounter(human.hand.cards)
    assert sum(counter.values()) == 6
    assert counter[copper] == 3
    assert counter[estate] == 2
    assert counter[curse] == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Patrol
    assert len(human.deck) >= 1
    assert human.deck.cards[-1].name == "Silver"
