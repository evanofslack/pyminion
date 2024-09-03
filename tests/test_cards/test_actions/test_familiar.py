from pyminion.expansions.alchemy import familiar
from pyminion.game import Game


def test_familiar(multiplayer_game: Game):
    player = multiplayer_game.players[0]

    player.hand.add(familiar)

    player.play(familiar, multiplayer_game)

    assert len(player.hand) == 6
    assert player.state.actions == 1

    for p in multiplayer_game.players:
        if p is not player:
            assert len(p.discard_pile) == 1
            assert p.discard_pile.cards[0].name == "Curse"
