from pyminion.expansions.base import copper, silver
from pyminion.expansions.intrigue import WishingWell, wishing_well
from pyminion.game import Game
from pyminion.human import Human


def test_wishing_well_correct_guess(human: Human, game: Game, monkeypatch):
    human.hand.add(wishing_well)
    human.deck.add(silver)
    human.deck.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "silver")

    human.play(wishing_well, game)
    hand_card_names = [c.name for c in human.hand.cards]
    assert len(human.hand) == 2
    assert "Copper" in hand_card_names
    assert "Silver" in hand_card_names
    assert human.deck.cards[-1].name != "Silver"
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is WishingWell
    assert human.state.actions == 1


def test_wishing_well_incorrect_guess(human: Human, game: Game, monkeypatch):
    human.hand.add(wishing_well)
    human.deck.add(silver)
    human.deck.add(copper)

    monkeypatch.setattr("builtins.input", lambda _: "copper")

    human.play(wishing_well, game)
    assert len(human.hand) == 1
    assert human.hand.cards[0].name == "Copper"
    assert human.deck.cards[-1].name == "Silver"
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is WishingWell
    assert human.state.actions == 1
