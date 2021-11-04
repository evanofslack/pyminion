from pyminion.models.core import Player
from pyminion.game import Game
from pyminion.models.base import Silver, Estate, vassal, smithy, estate, village


def test_vassal_not_action_play(player: Player, game: Game):
    player.hand.add(vassal)

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert player.state.actions == 0
    assert player.state.money == 2


def test_vassal_no_play(player: Player, game: Game, monkeypatch):
    player.deck.add(smithy)
    player.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert player.state.actions == 0
    assert player.state.money == 2


def test_vassal_play(player: Player, game: Game, monkeypatch):
    player.deck.add(smithy)
    player.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 3
    assert len(player.playmat) == 2
    assert len(player.discard_pile) == 0
    assert player.state.actions == 0
    assert player.state.money == 2


def test_vassal_play_chain_two(player: Player, game: Game, monkeypatch):
    # player.deck.add(vassal)
    player.deck.add(vassal)
    player.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 2
    assert len(player.discard_pile) == 1
    assert (player.discard_pile.cards[-1]) == estate
    assert player.state.actions == 0
    assert player.state.money == 4


def test_vassal_play_chain_three(player: Player, game: Game, monkeypatch):
    player.deck.add(vassal)
    player.deck.add(vassal)
    player.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 3
    assert len(player.discard_pile) == 1
    assert (player.discard_pile.cards[-1]) == estate
    assert player.state.actions == 0
    assert player.state.money == 6


def test_vassal_play_chain_smithy(player: Player, game: Game, monkeypatch):
    player.deck.add(smithy)
    player.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 3
    assert len(player.playmat) == 2
    assert len(player.discard_pile) == 0
    assert player.state.actions == 0
    assert player.state.money == 2


def test_vassal_play_chain_village(player: Player, game: Game, monkeypatch):
    player.deck.add(village)
    player.hand.add(vassal)

    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(player, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 2
    assert len(player.discard_pile) == 0
    assert player.state.actions == 2
    assert player.state.money == 2
