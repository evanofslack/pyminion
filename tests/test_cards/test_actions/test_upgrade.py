from pyminion.expansions.base import Copper, Estate, Silver, copper, estate
from pyminion.expansions.intrigue import Upgrade, upgrade
from pyminion.game import Game
from pyminion.human import Human


def test_upgrade(human: Human, game: Game, monkeypatch):
    human.hand.add(upgrade)
    human.hand.add(estate)

    responses = iter(["estate", "silver"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(upgrade, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Upgrade
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is Estate
    assert len(human.discard_pile) == 1
    assert type(human.discard_pile.cards[0]) is Silver
    assert human.state.actions == 1


def test_upgrade_no_gain(human: Human, game: Game, monkeypatch):
    human.hand.add(upgrade)
    human.hand.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "copper")

    human.play(upgrade, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Upgrade
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is Copper
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1


def test_upgrade_empty_hand(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()
    human.hand.add(upgrade)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop())

    human.play(upgrade, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Upgrade
    assert len(game.trash) == 0
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
