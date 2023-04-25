from pyminion.expansions.intrigue import MiningVillage, mining_village
from pyminion.game import Game
from pyminion.human import Human


def test_mining_village_no_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(mining_village)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    human.play(mining_village, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is MiningVillage
    assert len(game.trash) == 0
    assert human.state.actions == 2
    assert human.state.money == 0


def test_mining_village_trash(human: Human, game: Game, monkeypatch):
    human.hand.add(mining_village)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    human.play(mining_village, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 0
    assert len(game.trash) == 1
    assert type(game.trash.cards[0]) is MiningVillage
    assert human.state.actions == 2
    assert human.state.money == 2
