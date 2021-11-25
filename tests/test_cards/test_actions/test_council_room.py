from pyminion.game import Game
from pyminion.expansions.base import CouncilRoom, council_room


def test_council_room(multiplayer_game: Game):
    player = multiplayer_game.players[0]
    player.hand.add(council_room)
    assert len(player.hand) == 6
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.hand) == 5
    player.hand.cards[-1].play(player, multiplayer_game)
    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.hand) == 6
    assert len(player.hand) == 9
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is CouncilRoom
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 2
