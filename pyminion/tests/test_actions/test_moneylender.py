from pyminion.models.core import Turn, Player, Trash
from pyminion.models.base import Moneylender, Copper
from pyminion.expansions.base import moneylender, copper


def test_moneylender_normal(turn: Turn, player: Player, trash: Trash, monkeypatch):
    player.hand.add(moneylender)
    player.hand.add(copper)
    assert len(player.hand) == 2
    assert len(trash) == 0

    # mock decision = input() as "y" to trash card
    monkeypatch.setattr("builtins.input", lambda _: "y")

    player.hand.cards[0].play(turn, player, trash)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moneylender
    assert turn.actions == 0
    assert turn.money == 3
    assert len(trash) == 1
    assert type(trash.cards[0]) is Copper


def test_moneylender_no_input(turn: Turn, player: Player, trash: Trash, monkeypatch):
    player.hand.add(moneylender)
    player.hand.add(copper)
    assert len(player.hand) == 2
    assert len(trash) == 0

    # mock decision = input() as "n" to not trash card
    monkeypatch.setattr("builtins.input", lambda _: "n")

    player.hand.cards[0].play(turn, player, trash)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moneylender
    assert turn.actions == 0
    assert turn.money == 0
    assert len(trash) == 0


def test_moneylender_no_coppers(turn: Turn, player: Player, trash: Trash, monkeypatch):
    player.hand.add(moneylender)
    assert len(player.hand) == 1
    assert len(trash) == 0
    player.hand.cards[0].play(turn, player, trash)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Moneylender
    assert turn.actions == 0
    assert turn.money == 0
    assert len(trash) == 0
