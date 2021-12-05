from pyminion.bots import OptimizedBot
from pyminion.expansions.base import (
    Silver,
    copper,
    duchy,
    estate,
    gold,
    harbinger,
    province,
    silver,
)
from pyminion.game import Game
from pyminion.players import Human


def test_harbinger_valid_topdeck(human: Human, game: Game, monkeypatch):
    human.hand.add(harbinger)
    human.discard_pile.add(silver)

    monkeypatch.setattr("builtins.input", lambda _: "Silver")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert type(human.deck.cards[-1]) is Silver
