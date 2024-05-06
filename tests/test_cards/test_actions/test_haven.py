from pyminion.core import DeckCounter
from pyminion.expansions.base import Silver, silver
from pyminion.expansions.seaside import Haven, haven
from pyminion.game import Game
from pyminion.human import Human


def test_haven_set_aside(human: Human, game: Game, monkeypatch):
    human.deck.add(silver)
    human.hand.add(haven)

    responses = ["silver"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(haven, game)
    assert len(responses) == 0
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Haven
    assert len(human.set_aside) == 1
    assert type(human.set_aside.cards[0]) is Silver
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert human.playmat_persist_counts[haven.name] == 1

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Haven
    assert len(human.set_aside) == 1
    assert type(human.set_aside.cards[0]) is Silver
    assert len(human.discard_pile) == 0
    assert human.playmat_persist_counts[haven.name] == 1

    human.start_turn(game)

    assert len(human.hand) == 6
    counter = DeckCounter(human.hand.cards)
    assert counter[silver] == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Haven
    assert len(human.set_aside) == 0
    assert len(human.discard_pile) == 0
    assert human.playmat_persist_counts[haven.name] == 0

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
    assert len(human.playmat) == 0
    assert len(human.set_aside) == 0
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[haven] == 1
    assert human.playmat_persist_counts[haven.name] == 0


def test_haven_no_set_aside(human: Human, game: Game):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()
    human.hand.add(haven)

    human.play(haven, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Haven
    assert len(human.set_aside) == 0
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert len(human.playmat_persist_counts) == 0

    human.start_cleanup_phase(game)

    assert len(human.hand) == 1
    assert type(human.hand.cards[0]) is Haven
    assert len(human.playmat) == 0
    assert len(human.set_aside) == 0
    assert len(human.discard_pile) == 0
    assert len(human.playmat_persist_counts) == 0
