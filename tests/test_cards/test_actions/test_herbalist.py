from pyminion.expansions.base import gold
from pyminion.expansions.alchemy import alchemy_set, herbalist
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player
import pytest


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([herbalist])
def test_herbalist(player: Player, game: Game):
    player.hand.add(herbalist)

    player.play(herbalist, game)
    assert len(player.hand) == 0
    assert player.state.actions == 0
    assert player.state.buys == 2
    assert player.state.money == 1


@pytest.mark.expansions([alchemy_set])
@pytest.mark.kingdom_cards([herbalist])
def test_herbalist_topdeck(multiplayer_game: Game, monkeypatch):
    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    human.hand.add(herbalist)
    human.hand.add(gold)

    human.play(herbalist, multiplayer_game)
    human.play(gold, multiplayer_game)

    human.start_cleanup_phase(multiplayer_game)
    assert len(responses) == 0
    assert "Gold" in (card.name for card in human.hand)
    assert "Gold" not in (card.name for card in human.discard_pile)

    human.end_turn(multiplayer_game)
