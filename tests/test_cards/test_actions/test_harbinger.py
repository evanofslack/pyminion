from pyminion.models.core import Player
from pyminion.game import Game
from pyminion.models.base import Silver, harbinger, silver


def test_harbinger_valid_topdeck(player: Player, game: Game, monkeypatch):
    player.hand.add(harbinger)
    player.discard_pile.add(silver)

    monkeypatch.setattr("builtins.input", lambda _: "Silver")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 0
    assert player.state.actions == 1
    assert type(player.deck.cards[-1]) is Silver
