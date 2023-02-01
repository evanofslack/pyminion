from pyminion.expansions.base import (Bureaucrat, Estate, Silver, bureaucrat,
                                      copper, estate)
from pyminion.game import Game


def test_bureaucrat_topdecks_silver(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]
    player.hand.add(bureaucrat)
    assert len(player.hand) == 6

    monkeypatch.setattr("builtins.input", lambda _: "Estate")

    player.hand.cards[-1].play(player, multiplayer_game)
    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Bureaucrat
    assert type(player.deck.cards[-1]) is Silver
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1


def test_bureaucrat_opponent_topdecks_victory(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]
    player.hand.add(bureaucrat)
    opponent = multiplayer_game.players[1]
    opponent.hand.add(estate)
    assert len(opponent.hand) == 6
    assert len(opponent.deck) == 5

    monkeypatch.setattr("builtins.input", lambda _: "Estate")

    player.hand.cards[-1].play(player, multiplayer_game)
    assert len(opponent.hand) == 5
    assert len(opponent.deck) == 6
    assert type(opponent.deck.cards[-1]) is Estate


def test_bureaucrat_opponent_no_victory(multiplayer_game: Game, monkeypatch):
    player = multiplayer_game.players[0]
    player.hand.add(bureaucrat)
    opponent = multiplayer_game.players[1]
    opponent.hand.cards = [copper, copper]
    opp_hand_len = len(opponent.hand)

    player.hand.cards[-1].play(player, multiplayer_game)
    assert len(opponent.hand) == opp_hand_len


def test_bureaucrat_empty_silver(multiplayer_game: Game, monkeypatch):
    """
    with an empty silver pile, playing bureaucrat should only attack opponents

    """

    # empty the silver pile
    for pile in multiplayer_game.supply.piles:
        if pile.name == "Silver":
            pile.cards = []

    player = multiplayer_game.players[0]
    player.hand.add(bureaucrat)

    monkeypatch.setattr("builtins.input", lambda _: "Estate")
    player.hand.cards[-1].play(player, multiplayer_game)

    assert len(player.discard_pile) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Bureaucrat
    assert player.state.actions == 0
    assert player.state.money == 0
    assert player.state.buys == 1
