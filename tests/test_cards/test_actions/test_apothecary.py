from pyminion.expansions.base import copper, silver, gold, estate
from pyminion.expansions.alchemy import apothecary, potion
from pyminion.game import Game
from pyminion.human import Human


def test_apothecary(human: Human, game: Game, monkeypatch):
    human.deck.add(silver)
    human.deck.add(copper)
    human.deck.add(potion)
    human.deck.add(gold)
    human.deck.add(estate)

    human.hand.add(apothecary)

    responses = ["silver, gold"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(apothecary, game)
    assert len(responses) == 0
    assert len(human.hand) == 3
    hand_card_names = set(card.name for card in human.hand)
    assert hand_card_names == {"Estate", "Copper", "Potion"}
    assert len(human.deck) >= 2
    assert human.deck.cards[-1].name == "Gold"
    assert human.deck.cards[-2].name == "Silver"


def test_apothecary_1_topdeck(human: Human, game: Game, monkeypatch):
    human.deck.add(copper)
    human.deck.add(copper)
    human.deck.add(potion)
    human.deck.add(gold)
    human.deck.add(estate)

    human.hand.add(apothecary)

    responses = []
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.play(apothecary, game)
    assert len(responses) == 0
    assert len(human.hand) == 4
    hand_card_names = set(card.name for card in human.hand)
    assert hand_card_names == {"Estate", "Copper", "Potion"}
    assert len(human.deck) >= 1
    assert human.deck.cards[-1].name == "Gold"
