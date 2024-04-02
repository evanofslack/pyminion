from pyminion.expansions.base import curse, estate, silver
from pyminion.expansions.seaside import lookout
from pyminion.game import Game
from pyminion.human import Human


def test_lookout_3_cards(human: Human, game: Game, monkeypatch):
    human.deck.add(silver)
    human.deck.add(curse)
    human.deck.add(estate)

    human.hand.add(lookout)

    responses = ["curse", "estate"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(lookout, game)
    assert len(responses) == 0
    assert human.state.actions == 1
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Curse"
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Estate"
    assert len(human.deck) >= 1
    assert human.deck.cards[-1].name == "Silver"


def test_lookout_no_cards(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.hand.add(lookout)

    human.play(lookout, game)
    assert human.state.actions == 1
    assert len(game.trash) == 0
    assert len(human.discard_pile) == 0
    assert len(human.deck) == 0


def test_lookout_1_card(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()
    human.deck.add(silver)

    human.hand.add(lookout)

    human.play(lookout, game)
    assert human.state.actions == 1
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Silver"
    assert len(human.discard_pile) == 0
    assert len(human.deck) == 0


def test_lookout_2_cards(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()
    human.deck.add(silver)
    human.deck.add(estate)

    human.hand.add(lookout)

    responses = ["estate"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(lookout, game)
    assert len(responses) == 0
    assert human.state.actions == 1
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Estate"
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Silver"
    assert len(human.deck) == 0
