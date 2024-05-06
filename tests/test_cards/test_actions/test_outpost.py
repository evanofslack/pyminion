from pyminion.core import DeckCounter
from pyminion.expansions.base import silver, gold, curse
from pyminion.expansions.seaside import outpost
from pyminion.game import Game


def test_outpost(multiplayer_game: Game, monkeypatch):
    responses = [
        "outpost", # 1st turn action
        "",        # 1st turn treasure
        "",        # 1st turn buy
        "",        # 2nd turn treasure
        "",        # 2nd turn buy
    ]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    player = multiplayer_game.players[0]
    player.hand.cards.clear()

    # should not draw this card
    player.deck.add(curse)

    # cards for extra turn
    player.deck.add(silver)
    player.deck.add(silver)
    player.deck.add(silver)

    # cards for main turn
    player.hand.add(outpost)
    player.hand.add(gold)

    multiplayer_game.play_turn(player)
    assert len(responses) == 0
    assert player.turns == 1
    assert len(player.hand) == 5
    assert len(player.discard_pile) == 5
    counter = DeckCounter(player.discard_pile)
    assert counter[outpost] == 1
    assert counter[silver] == 3
    assert counter[gold] == 1


def test_outpost_next_turn(multiplayer_game: Game, monkeypatch):
    responses = [
        "outpost", # 1st turn action
        "",        # 1st turn treasure
        "",        # 1st turn buy
        "outpost", # 2nd turn action
        "",        # 2nd turn treasure
        "",        # 2nd turn buy
    ]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    player = multiplayer_game.players[0]
    player.hand.cards.clear()

    # should not draw this card
    player.deck.add(curse)

    # cards for extra turn
    player.deck.add(outpost)
    player.deck.add(silver)
    player.deck.add(silver)

    # cards for main turn
    player.hand.add(outpost)
    player.hand.add(gold)

    multiplayer_game.play_turn(player)
    assert len(responses) == 0
    assert player.turns == 1
    assert len(player.hand) == 3
    assert len(player.playmat) == 1
    assert player.playmat.cards[0].name == "Outpost"
    assert len(player.discard_pile) == 4
    counter = DeckCounter(player.discard_pile)
    assert counter[outpost] == 1
    assert counter[silver] == 2
    assert counter[gold] == 1
