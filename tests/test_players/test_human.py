from pyminion.expansions.base import copper, moat, witch
from pyminion.game import Game
from pyminion.human import Human, get_matches
import pytest


def test_get_matches_all_match():
    names = ["Market", "Masquerade", "Merchant"]
    matches = get_matches("m", names)
    assert matches == ["Market", "Masquerade", "Merchant"]

    names = ["Market", "Masquerade", "Merchant"]
    matches = get_matches("M", names)
    assert matches == ["Market", "Masquerade", "Merchant"]


def test_get_matches_partial_match():
    names = ["Market", "Masquerade", "Merchant"]
    matches = get_matches("ma", names)
    assert matches == ["Market", "Masquerade"]


def test_get_matches_no_match():
    names = ["Market", "Masquerade", "Merchant"]
    matches = get_matches("x", names)
    assert matches == []


def test_get_matches_multi_word():
    names = ["King's Cache", "King's Castle", "King's Court"]
    matches = get_matches("k", names)
    assert matches == ["King's Cache", "King's Castle", "King's Court"]

    names = ["King's Cache", "King's Castle", "King's Court"]
    matches = get_matches("king's ca", names)
    assert matches == ["King's Cache", "King's Castle"]

    names = ["King's Cache", "King's Castle", "King's Court"]
    matches = get_matches("k ca", names)
    assert matches == ["King's Cache", "King's Castle"]

    names = ["King's Cache", "King's Castle", "King's Court"]
    matches = get_matches("k cas", names)
    assert matches == ["King's Castle"]


def test_get_matches_multi_word_exact_match():
    names = ["Market", "Market Square"]
    matches = get_matches("marke", names)
    assert matches == ["Market", "Market Square"]

    names = ["Market", "Market Square"]
    matches = get_matches("market", names)
    assert matches == ["Market"]


def test_yes_input(human: Human, game: Game, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert human.decider.binary_decision(prompt="test", card=copper, player=human, game=game) is True
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    assert human.decider.binary_decision(prompt="test", card=copper, player=human, game=game) is True


def test_no_input(human: Human, game: Game, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert human.decider.binary_decision(prompt="test", card=copper, player=human, game=game) is False
    monkeypatch.setattr("builtins.input", lambda _: "no")
    assert human.decider.binary_decision(prompt="test", card=copper, player=human, game=game) is False


@pytest.mark.kingdom_cards([moat])
def test_is_attacked_no_moat(multiplayer_game: Game, monkeypatch):
    human = multiplayer_game.players[0]
    assert isinstance(human, Human)
    assert human.is_attacked(attacking_player=human, attack_card=witch, game=multiplayer_game)


@pytest.mark.kingdom_cards([moat])
def test_is_attacked_yes_moat(multiplayer_game: Game, monkeypatch):
    human = multiplayer_game.players[0]
    assert isinstance(human, Human)
    human.deck.add(card=moat)
    human.draw()
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    assert not human.is_attacked(attacking_player=human, attack_card=witch, game=multiplayer_game)


def test_action_phase_no_actions(human: Human, game: Game):
    assert not human.start_action_phase(game)


def test_action_phase_no_input(human: Human, monkeypatch):
    human.hand.add(moat)
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert len(human.playmat) == 0


def test_action_phase_play_action(human: Human, game: Game, monkeypatch):
    human.hand.add(moat)
    monkeypatch.setattr("builtins.input", lambda _: "moat")
    human.start_action_phase(game)
    assert len(human.playmat) == 1


def test_treasure_phase_no_treasures(human: Human, game: Game):
    assert not human.start_treasure_phase(game)


def test_treasure_phase_one_copper(human: Human, game: Game, monkeypatch):
    human.hand.add(copper)
    monkeypatch.setattr("builtins.input", lambda _: "copper")
    human.start_treasure_phase(game)
    assert human.state.money == 1
    assert human.playmat.cards[0].name == "Copper"


def test_treasure_phase_autoplay(human: Human, game: Game, monkeypatch):
    for _ in range(3):
        human.hand.add(copper)
    monkeypatch.setattr("builtins.input", lambda _: "all")
    human.start_treasure_phase(game)
    assert human.state.money == 3


def test_buy_phase_no_buys(human: Human, game: Game):
    human.state.buys = 0
    assert not human.start_buy_phase(game)


def test_buy_phase_no_input(human: Human, monkeypatch):
    human.state.money = 2
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert not human.discard_pile.cards


def test_buy_phase_input_estate(human: Human, game: Game, monkeypatch):
    human.state.money = 2
    monkeypatch.setattr("builtins.input", lambda _: "estate")
    human.start_buy_phase(game)
    assert human.state.money == 0
    assert human.discard_pile.cards[-1].name == "Estate"
