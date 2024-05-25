from pyminion.expansions.base import chapel, copper
from pyminion.expansions.alchemy import apprentice, golem
from pyminion.game import Game
from pyminion.human import Human


def test_apprentice_money_cost(human: Human, game: Game, monkeypatch):
    human.hand.add(apprentice)
    human.hand.add(chapel)
    human.hand.add(copper)
    assert len(human.hand) == 3

    responses = ["chapel"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(apprentice, game)
    assert len(responses) == 0
    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Apprentice"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Chapel"
    assert human.state.actions == 1


def test_apprentice_money_potion_cost(human: Human, game: Game, monkeypatch):
    human.hand.add(apprentice)
    human.hand.add(golem)
    human.hand.add(copper)
    assert len(human.hand) == 3

    responses = ["golem"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(apprentice, game)
    assert len(responses) == 0
    assert len(human.hand) == 7
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Apprentice"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Golem"
    assert human.state.actions == 1


def test_apprentice_no_cards(human: Human, game: Game, monkeypatch):
    human.hand.add(apprentice)
    assert len(human.hand) == 1

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(apprentice, game)
    assert len(responses) == 0
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Apprentice"
    assert len(game.trash) == 0
    assert human.state.actions == 1


def test_apprentice_one_card(human: Human, game: Game, monkeypatch):
    human.hand.add(apprentice)
    human.hand.add(golem)
    assert len(human.hand) == 2

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(apprentice, game)
    assert len(responses) == 0
    assert len(human.hand) == 6
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Apprentice"
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Golem"
    assert human.state.actions == 1
