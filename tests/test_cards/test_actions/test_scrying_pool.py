from pyminion.expansions.base import silver, gold, smithy, village
from pyminion.expansions.alchemy import familiar, scrying_pool
from pyminion.game import Game


def test_scrying_pool(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.deck.add(silver)
    p1.hand.add(scrying_pool)

    p2.deck.add(gold)

    responses = ["n", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1.play(scrying_pool, multiplayer_game)
    assert len(responses) == 0

    assert p1.state.actions == 1
    assert len(p1.hand) == 6
    assert "Silver" in (card.name for card in p1.hand)
    assert len(p1.discard_pile) == 0

    assert len(p2.discard_pile) == 1
    assert p2.discard_pile.cards[0].name == "Gold"


def test_scrying_pool_no_draw(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.deck.cards.clear()
    p1.hand.add(scrying_pool)

    p2.deck.add(gold)

    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1.play(scrying_pool, multiplayer_game)
    assert len(responses) == 0

    assert p1.state.actions == 1
    assert len(p1.hand) == 5
    assert len(p1.discard_pile) == 0

    assert len(p2.deck) > 0
    assert p2.deck.cards[-1].name == "Gold"
    assert len(p2.discard_pile) == 0


def test_scrying_pool_multiple_actions(multiplayer_game: Game, monkeypatch):
    players = multiplayer_game.players
    p1 = players[0]
    p2 = players[1]

    p1.deck.add(silver)
    p1.deck.add(smithy)
    p1.deck.add(village)
    p1.deck.add(familiar)
    p1.hand.add(scrying_pool)

    p2.deck.add(gold)

    responses = ["n", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    p1.play(scrying_pool, multiplayer_game)
    assert len(responses) == 0

    assert p1.state.actions == 1
    assert len(p1.hand) == 9
    assert {"Silver", "Smithy", "Village", "Familiar"}.issubset(card.name for card in p1.hand)
    assert len(p1.discard_pile) == 0

    assert len(p2.discard_pile) == 1
    assert p2.discard_pile.cards[0].name == "Gold"
