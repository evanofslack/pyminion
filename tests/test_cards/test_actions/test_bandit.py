from pyminion.game import Game
from pyminion.models.base import Bandit, Gold, bandit, copper, gold, silver


def test_bandit_gains_gold(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(bandit)
    assert len(player.hand) == 6
    player.hand.cards[-1].play(player, multiplayer_game)
    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Bandit
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is Gold
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1


def test_bandit_trash_one_silver(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(bandit)
    assert len(player.hand) == 6
    # for p in multiplayer_game.players:
    #     if p is not player:
    #         assert len(p.discard_pile) == 0
    player.hand.cards[-1].play(player, multiplayer_game)
    # for p in multiplayer_game.players:
    #     if p is not player:
    #         assert len(p.discard_pile) == 1
    #         assert p.discard_pile.cards[-1] is curse
    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Bandit
    assert len(player.discard_pile) == 1
    assert type(player.discard_pile.cards[0]) is Gold
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1
