from pyminion.expansions.base import copper, moat, witch
from pyminion.game import Game
from pyminion.players import Human


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


def test_is_attacked_no_moat(human: Human, game: Game, monkeypatch):
    assert human.is_attacked(player=human, attack_card=witch, game=game)


def test_is_attacked_yes_moat(human: Human, game: Game, monkeypatch):
    human.hand.add(card=moat)
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    assert not human.is_attacked(player=human, attack_card=witch, game=game)


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
