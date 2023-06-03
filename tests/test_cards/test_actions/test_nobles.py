from pyminion.expansions.intrigue import nobles
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_nobles_cards(human: Human, game: Game, monkeypatch):
    human.hand.add(nobles)

    monkeypatch.setattr("builtins.input", lambda _: "1")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 3
    assert len(human.playmat) == 1
    assert human.state.actions == 0


def test_nobles_actions(human: Human, game: Game, monkeypatch):
    human.hand.add(nobles)

    monkeypatch.setattr("builtins.input", lambda _: "2")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.state.actions == 2


def test_nobles_vp(player: Player):
    player.hand.add(nobles)
    assert player.hand.cards[0].score(player) == 2
    assert player.get_victory_points() == 5
    player.deck.add(nobles)
    player.discard_pile.add(nobles)
    assert player.get_victory_points() == 9
