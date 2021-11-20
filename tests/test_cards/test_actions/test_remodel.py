from pyminion.game import Game
from pyminion.models.base import copper, remodel
from pyminion.players import Human


def test_remodel_gain_valid(human: Human, game: Game, monkeypatch):
    human.hand.add(copper)
    human.hand.add(remodel)
    assert len(human.discard_pile) == 0
    assert len(game.trash) == 0

    responses = iter(["copper", "estate"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.hand.cards[-1].play(human, game)
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.discard_pile.cards[0].name == "Estate"
    assert game.trash.cards[0].name == "Copper"
