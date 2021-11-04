from pyminion.models.core import Player
from pyminion.game import Game
from pyminion.models.base import Estate, workshop


def test_workshop_gain_valid(player: Player, game: Game, monkeypatch):
    player.hand.add(workshop)
    assert len(player.discard_pile) == 0

    # mock decision = input() as "Copper" to discard
    monkeypatch.setattr("builtins.input", lambda _: "Estate")

    player.hand.cards[0].play(player, game)
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert player.state.actions == 0
    assert type(player.discard_pile.cards[0]) is Estate
    assert len(game.supply.piles[3]) == 4
