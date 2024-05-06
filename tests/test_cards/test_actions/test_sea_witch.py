from pyminion.core import DeckCounter
from pyminion.expansions.base import Curse, copper
from pyminion.expansions.seaside import SeaWitch, sea_witch
from pyminion.game import Game


def test_sea_witch(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]

    for _ in range(9):
        player.deck.add(copper)

    player.hand.add(sea_witch)
    assert len(player.hand) == 6

    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 0

    player.play(sea_witch, multiplayer_game)

    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 1
            assert type(p.discard_pile.cards[0]) is Curse

    assert len(player.hand) == 7
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is SeaWitch
    assert player.state.actions == 0
    assert player.playmat_persist_counts[sea_witch.name] == 1

    player.start_cleanup_phase(multiplayer_game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is SeaWitch
    assert len(player.discard_pile) == 7
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[sea_witch] == 0
    assert player.playmat_persist_counts[sea_witch.name] == 1

    responses = ["copper, copper"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    player.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is SeaWitch
    assert len(player.discard_pile) == 9
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[sea_witch] == 0
    assert player.playmat_persist_counts[sea_witch.name] == 0

    player.start_cleanup_phase(multiplayer_game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[sea_witch] == 1
    assert player.playmat_persist_counts[sea_witch.name] == 0
