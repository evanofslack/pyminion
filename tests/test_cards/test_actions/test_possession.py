from pyminion.expansions.base import chapel, copper, silver
from pyminion.expansions.alchemy import possession
from pyminion.game import Game


def test_possession(multiplayer_game: Game, monkeypatch):
    responses = [
        "possession",           # player's turn: play possession
        "",                     # player's turn: no treasures to play
        "copper,copper,copper", # possession turn: play treasures
        "silver",               # possession turn: buy silver
    ]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    player = multiplayer_game.players[0]
    player.hand.cards.clear()
    player.hand.add(possession)

    opponent = multiplayer_game.players[1]
    opponent.hand.cards.clear()
    for _ in range(3):
        opponent.hand.add(copper)

    assert "Silver" not in (card.name for card in player.get_all_cards())
    assert "Silver" not in (card.name for card in opponent.get_all_cards())

    multiplayer_game.play_turn(player)

    assert len(responses) == 0
    assert "Silver" in (card.name for card in player.get_all_cards())
    assert "Silver" not in (card.name for card in opponent.get_all_cards())


def test_possession_trash(multiplayer_game: Game, monkeypatch):
    responses = [
        "possession", # player's turn: play possession
        "",           # player's turn: no treasures to play
        "chapel",     # possession turn: play chapel
        "silver",     # possession turn: trash silver
        "",           # possession turn: do not buy anything
    ]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    player = multiplayer_game.players[0]
    player.hand.cards.clear()
    player.hand.add(possession)

    opponent = multiplayer_game.players[1]
    opponent.hand.cards.clear()
    opponent.hand.add(silver)
    opponent.hand.add(chapel)

    assert "Silver" in (card.name for card in opponent.hand)

    multiplayer_game.play_turn(player)

    assert len(responses) == 0
    assert len(multiplayer_game.trash) == 0
    assert "Silver" in (card.name for card in opponent.discard_pile)
