from pyminion.expansions.base import estate, throne_room, silver
from pyminion.expansions.seaside import treasury
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_treasury_play(player: Player, game: Game):
    player.hand.add(treasury)

    assert len(player.hand) == 1

    player.play(treasury, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert player.playmat.cards[0].name == "Treasury"
    assert player.state.actions == 1
    assert player.state.money == 1


def test_treasury_topdeck_yes(human: Human, game: Game, monkeypatch):
    responses = ["", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    # Topdeck an estate. This way, the player will draw it with treasury
    # and there will not be prompting to play treasures.
    human.deck.add(estate)

    human.hand.add(treasury)

    human.play(treasury, game)
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Treasury"

    human.start_treasure_phase(game)
    assert game.current_phase == Game.Phase.Buy

    # gain a non-victory card
    human.gain(silver, game)

    human.start_buy_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 0
    assert human.deck.cards[-1].name == "Treasury"


def test_treasury_topdeck_no(human: Human, game: Game, monkeypatch):
    responses = ["", "n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    # Topdeck an estate. This way, the player will draw it with treasury
    # and there will not be prompting to play treasures.
    human.deck.add(estate)

    human.hand.add(treasury)

    human.play(treasury, game)
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Treasury"

    human.start_treasure_phase(game)
    assert game.current_phase == Game.Phase.Buy

    # gain a non-victory card
    human.gain(silver, game)

    human.start_buy_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Treasury"
    assert human.deck.cards[-1].name != "Treasury"


def test_treasury_victory_in_buy_phase(human: Human, game: Game, monkeypatch):
    responses = [""]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    # Topdeck an estate. This way, the player will draw it with treasury
    # and there will not be prompting to play treasures.
    human.deck.add(estate)

    human.hand.add(treasury)

    human.play(treasury, game)
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Treasury"

    human.start_treasure_phase(game)
    assert game.current_phase == Game.Phase.Buy

    # gain a victory card
    human.gain(estate, game)

    human.start_buy_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Treasury"
    assert human.deck.cards[-1].name != "Treasury"


def test_treasury_victory_not_in_buy_phase(human: Human, game: Game, monkeypatch):
    responses = ["", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    # Topdeck an estate. This way, the player will draw it with treasury
    # and there will not be prompting to play treasures.
    human.deck.add(estate)

    human.hand.add(treasury)

    human.play(treasury, game)
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Treasury"

    assert game.current_phase == Game.Phase.Action

    # gain a victory card
    human.gain(estate, game)

    human.start_treasure_phase(game)
    assert game.current_phase == Game.Phase.Buy

    human.start_buy_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 0
    assert human.deck.cards[-1].name == "Treasury"


def test_treasury_throne_room(human: Human, game: Game, monkeypatch):
    responses = ["Treasury", "", "y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    # Topdeck estates. This way, the player will draw them with treasury
    # and there will not be prompting to play treasures.
    human.deck.add(estate)
    human.deck.add(estate)

    human.hand.add(throne_room)
    human.hand.add(treasury)

    human.play(throne_room, game)
    assert len(human.hand) == 2
    assert len(human.playmat) == 2
    assert human.playmat.cards[0].name == "Throne Room"
    assert human.playmat.cards[1].name == "Treasury"
    assert human.state.actions == 2
    assert human.state.money == 2

    human.start_treasure_phase(game)
    assert game.current_phase == Game.Phase.Buy

    # gain a non-victory card
    human.gain(silver, game)

    human.start_buy_phase(game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Throne Room"
    assert human.deck.cards[-1].name == "Treasury"
    assert human.deck.cards[-2].name != "Treasury"
