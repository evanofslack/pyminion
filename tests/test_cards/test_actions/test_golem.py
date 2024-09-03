from pyminion.expansions.base import chapel, copper, estate, silver
from pyminion.expansions.alchemy import golem
from pyminion.game import Game
from pyminion.human import Human


def test_golem(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.deck.add(copper)
    human.deck.add(golem)
    human.deck.add(estate)
    human.deck.add(chapel)
    human.deck.add(silver)

    human.discard_pile.add(chapel)

    human.hand.add(golem)

    responses = ["1"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(golem, game)
    assert len(responses) == 0
    assert len(human.playmat) == 3
    assert sorted(card.name for card in human.playmat) == ["Chapel", "Chapel", "Golem"]
    assert len(human.hand) == 0
    assert len(human.deck) == 0
    assert len(human.discard_pile) == 4
    assert sorted(card.name for card in human.discard_pile) == ["Copper", "Estate", "Golem", "Silver"]
    assert human.state.actions == 0


def test_golem_choose_other_card(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.deck.add(copper)
    human.deck.add(golem)
    human.deck.add(estate)
    human.deck.add(chapel)
    human.deck.add(silver)

    human.discard_pile.add(chapel)

    human.hand.add(golem)

    responses = ["2"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(golem, game)
    assert len(responses) == 0
    assert len(human.playmat) == 3
    assert sorted(card.name for card in human.playmat) == ["Chapel", "Chapel", "Golem"]
    assert len(human.hand) == 0
    assert len(human.deck) == 0
    assert len(human.discard_pile) == 4
    assert sorted(card.name for card in human.discard_pile) == ["Copper", "Estate", "Golem", "Silver"]
    assert human.state.actions == 0


def test_golem_no_actions(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.deck.add(copper)
    human.deck.add(estate)
    human.deck.add(silver)

    human.hand.add(golem)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(golem, game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Golem"
    assert len(human.hand) == 0
    assert len(human.deck) == 0
    assert len(human.discard_pile) == 3
    assert sorted(card.name for card in human.discard_pile) == ["Copper", "Estate", "Silver"]
    assert human.state.actions == 0


def test_golem_one_action(human: Human, game: Game, monkeypatch):
    human.deck.cards.clear()
    human.discard_pile.cards.clear()

    human.deck.add(copper)
    human.deck.add(golem)
    human.deck.add(estate)
    human.deck.add(silver)

    human.discard_pile.add(chapel)

    human.hand.add(golem)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(golem, game)
    assert len(responses) == 0
    assert len(human.playmat) == 2
    assert sorted(card.name for card in human.playmat) == ["Chapel", "Golem"]
    assert len(human.hand) == 0
    assert len(human.deck) == 0
    assert len(human.discard_pile) == 4
    assert sorted(card.name for card in human.discard_pile) == ["Copper", "Estate", "Golem", "Silver"]
    assert human.state.actions == 0
