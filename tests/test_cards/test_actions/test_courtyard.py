from pyminion.expansions.base import Duchy, duchy
from pyminion.expansions.intrigue import courtyard
from pyminion.game import Game
from pyminion.human import Human

def test_courtyard_topdeck(human: Human, game: Game, monkeypatch):
    human.hand.add(courtyard)
    human.hand.add(duchy)
    assert len(human.deck) == 10
    assert len(human.hand) == 2

    monkeypatch.setattr("builtins.input", lambda _: "Duchy")

    human.play(courtyard, game)
    assert len(human.deck) == 8
    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert type(human.deck.cards[-1]) is Duchy
