from pyminion.expansions.base import Silver, harbinger, silver
from pyminion.game import Game
from pyminion.human import Human


def test_harbinger_valid_topdeck(human: Human, game: Game, monkeypatch):
    human.hand.add(harbinger)
    human.discard_pile.add(silver)

    monkeypatch.setattr("builtins.input", lambda _: "Silver")

    human.play(harbinger, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert type(human.deck.cards[-1]) is Silver


def test_harbinger_empty_discard_pile(human: Human, game: Game):
    human.hand.add(harbinger)
    assert len(human.discard_pile) == 0
    assert len(human.deck) == 10

    human.play(harbinger, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert len(human.deck) == 9
    assert human.state.actions == 1
