from pyminion.core import DeckCounter
from pyminion.expansions.base import copper, throne_room
from pyminion.expansions.seaside import Caravan, caravan
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_caravan(player: Player, game: Game):
    for _ in range(5):
        player.deck.add(copper)
    player.hand.add(caravan)

    player.play(caravan, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Caravan
    assert len(player.discard_pile) == 0
    assert player.state.actions == 1
    assert player.playmat_persist_counts[caravan.name] == 1

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Caravan
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is not Caravan
    assert player.playmat_persist_counts[caravan.name] == 1

    player.start_turn(game)

    assert len(player.hand) == 6
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Caravan
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is not Caravan
    assert player.playmat_persist_counts[caravan.name] == 0

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[caravan] == 1
    assert player.playmat_persist_counts[caravan.name] == 0


def test_caravan_throne_room(human: Human, game: Game, monkeypatch):
    for _ in range(5):
        human.deck.add(copper)
    human.hand.add(caravan)
    human.hand.add(throne_room)

    responses = iter(["Caravan"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(throne_room, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 2
    counter = DeckCounter(human.playmat.cards)
    assert counter[throne_room] == 1
    assert counter[caravan] == 1
    assert len(human.discard_pile) == 0
    assert human.state.actions == 2
    assert human.playmat_persist_counts[caravan.name] == 1
    assert human.playmat_persist_counts[throne_room.name] == 1

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
    assert len(human.playmat) == 2
    counter = DeckCounter(human.playmat.cards)
    assert counter[throne_room] == 1
    assert counter[caravan] == 1
    assert len(human.discard_pile) == 2
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[throne_room] == 0
    assert counter[caravan] == 0

    human.start_turn(game)

    assert len(human.hand) == 7
    assert len(human.playmat) == 2
    counter = DeckCounter(human.playmat.cards)
    assert counter[throne_room] == 1
    assert counter[caravan] == 1
    assert len(human.discard_pile) == 2
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[throne_room] == 0
    assert counter[caravan] == 0

    human.start_cleanup_phase(game)

    assert len(human.hand) == 5
    assert len(human.playmat) == 0
    counter = DeckCounter(human.discard_pile.cards)
    assert counter[caravan] == 1
    assert counter[throne_room] == 1
