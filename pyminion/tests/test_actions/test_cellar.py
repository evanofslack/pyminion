from pyminion.models.core import Turn, Player, Trash
from pyminion.models.base import Cellar, Copper, Estate, cellar, copper, estate


def test_moneylender_discard_one(turn: Turn, player: Player, trash: Trash, monkeypatch):
    player.hand.add(cellar)
    player.hand.add(copper)
    player.hand.add(copper)
    assert len(player.hand) == 3
    assert len(player.discard_pile) == 0

    # mock decision = input() as "y" to trash card
    monkeypatch.setattr("builtins.input", lambda _: "Copper")

    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 2
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 1
    assert type(player.playmat.cards[0]) is Cellar
    assert turn.actions == 1
    assert type(player.discard_pile.cards[0]) is Copper


def test_moneylender_discard_multiple(
    turn: Turn, player: Player, trash: Trash, monkeypatch
):
    player.hand.add(cellar)
    player.hand.add(copper)
    player.hand.add(copper)
    player.hand.add(estate)
    assert len(player.hand) == 4
    assert len(player.discard_pile) == 0

    # mock decision = input() as "y" to trash card
    monkeypatch.setattr("builtins.input", lambda _: "Copper, Estate")

    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 3
    assert len(player.playmat) == 1
    assert len(player.discard_pile) == 2
    assert type(player.playmat.cards[0]) is Cellar
    assert turn.actions == 1
    assert type(player.discard_pile.cards[0]) is Copper
    assert type(player.discard_pile.cards[1]) is Estate


# def test_moneylender_no_input(turn: Turn, player: Player, trash: Trash, monkeypatch):
#     player.hand.add(moneylender)
#     player.hand.add(copper)
#     assert len(player.hand) == 2
#     assert len(trash) == 0

#     # mock decision = input() as "n" to not trash card
#     monkeypatch.setattr("builtins.input", lambda _: "n")

#     player.hand.cards[0].play(turn, player, trash)
#     assert len(player.hand) == 1
#     assert len(player.playmat) == 1
#     assert type(player.playmat.cards[0]) is Moneylender
#     assert turn.actions == 0
#     assert turn.money == 0
#     assert len(trash) == 0


# def test_moneylender_no_coppers(turn: Turn, player: Player, trash: Trash, monkeypatch):
#     player.hand.add(moneylender)
#     assert len(player.hand) == 1
#     assert len(trash) == 0
#     player.hand.cards[0].play(turn, player, trash)
#     assert len(player.hand) == 0
#     assert len(player.playmat) == 1
#     assert type(player.playmat.cards[0]) is Moneylender
#     assert turn.actions == 0
#     assert turn.money == 0
#     assert len(trash) == 0
