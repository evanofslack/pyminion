from pyminion.core import DeckCounter
from pyminion.expansions.seaside import FishingVillage, fishing_village
from pyminion.game import Game
from pyminion.player import Player


def test_fishing_village(player: Player, game: Game):
    player.hand.add(fishing_village)

    player.play(fishing_village, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is FishingVillage
    assert len(player.discard_pile) == 0
    assert player.state.actions == 2
    assert player.state.money == 1
    assert player.playmat_persist_counts[fishing_village.name] == 1

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is FishingVillage
    assert len(player.discard_pile) == 0
    assert player.playmat_persist_counts[fishing_village.name] == 1

    player.start_turn(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is FishingVillage
    assert len(player.discard_pile) == 0
    assert player.state.actions == 2
    assert player.state.money == 1
    assert player.playmat_persist_counts[fishing_village.name] == 0

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[fishing_village] == 1
    assert player.playmat_persist_counts[fishing_village.name] == 0
