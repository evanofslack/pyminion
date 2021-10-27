from pyminion.models.core import Player, Game
from pyminion.models.base import Workshop, Copper, Estate, workshop, copper, estate


def test_workshop_gain_valid(player: Player, game: Game, monkeypatch):
    player.hand.add(workshop)
    assert len(player.discard_pile) == 0

    # mock decision = input() as "Copper" to discard
    monkeypatch.setattr("builtins.input", lambda _: "Copper")

    player.hand.cards[0].play(player, game)
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert player.state.actions == 0
    assert type(player.discard_pile.cards[0]) is Copper
