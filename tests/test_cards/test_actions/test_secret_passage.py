from pyminion.expansions.base import copper, silver
from pyminion.expansions.intrigue import SecretPassage, secret_passage
from pyminion.game import Game
from pyminion.human import Human


def test_secret_passage_top(human: Human, game: Game, monkeypatch):
    human.hand.add(secret_passage)
    human.hand.add(silver)

    assert len(human.deck) == 10

    responses = iter(["silver", "9"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(secret_passage, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is SecretPassage
    assert len(human.deck) == 9
    assert human.deck.cards[-1].name == "Silver"


def test_secret_passage_middle(human: Human, game: Game, monkeypatch):
    human.hand.add(secret_passage)
    human.hand.add(silver)

    assert len(human.deck) == 10

    responses = iter(["silver", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(secret_passage, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is SecretPassage
    assert len(human.deck) == 9
    assert human.deck.cards[4].name == "Silver"


def test_secret_passage_bottom(human: Human, game: Game, monkeypatch):
    human.hand.add(secret_passage)
    human.hand.add(silver)

    assert len(human.deck) == 10

    responses = iter(["silver", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(secret_passage, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is SecretPassage
    assert len(human.deck) == 9
    assert human.deck.cards[0].name == "Silver"


def test_secret_passage_no_ask(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.hand.add(secret_passage)
    human.hand.add(silver)

    assert len(human.deck) == 0

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(secret_passage, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is SecretPassage
    assert len(human.deck) == 1
    assert human.deck.cards[0].name == "Silver"


def test_secret_passage_no_cards(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.hand.add(secret_passage)

    assert len(human.deck) == 0

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(secret_passage, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is SecretPassage
    assert len(human.deck) == 0
