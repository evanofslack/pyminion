from pyminion.core import DeckCounter
from pyminion.expansions.base import copper
from pyminion.expansions.seaside import TidePools, tide_pools
from pyminion.game import Game
from pyminion.human import Human


def test_tide_pools(human: Human, game: Game, monkeypatch):
    for _ in range(8):
        human.deck.add(copper)

    human.hand.add(tide_pools)

    responses = iter(["copper, copper"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(tide_pools, game)
    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TidePools
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert human.playmat_persist_counts[tide_pools.name] == 1

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TidePools
    assert len(human.discard_pile) == 3
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[tide_pools] == 0
    assert human.playmat_persist_counts[tide_pools.name] == 1

    human.start_turn(game)

    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TidePools
    assert len(human.discard_pile) == 5
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[tide_pools] == 0
    assert human.playmat_persist_counts[tide_pools.name] == 0

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
    assert len(human.playmat) == 0
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[tide_pools] == 1
    assert human.playmat_persist_counts[tide_pools.name] == 0


def test_tide_pools_multiple(human: Human, game: Game, monkeypatch):
    for _ in range(17):
        human.deck.add(copper)
    for _ in range(4):
        human.hand.add(tide_pools)

    responses = ["copper, copper", "copper, copper"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop())

    for _ in range(4):
        human.play(tide_pools, game)
    assert len(human.hand) == 12

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5

    human.start_turn(game)

    assert len(human.hand) == 0
    assert len(responses) == 0

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
