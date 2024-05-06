from pyminion.expansions.base import throne_room
from pyminion.expansions.seaside import treasure_map
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_treasure_map_one(player: Player, game: Game):
    player.hand.add(treasure_map)
    assert len(player.deck) == 10

    player.play(treasure_map, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 0
    assert len(player.deck) == 10
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Treasure Map"
    assert player.state.actions == 0


def test_treasure_map_two(player: Player, game: Game):
    player.hand.add(treasure_map)
    player.hand.add(treasure_map)
    assert len(player.deck) == 10

    player.play(treasure_map, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 0
    assert len(player.deck) == 14
    for i in range(4):
        assert player.deck.cards[-1 - i].name == "Gold"
    assert len(game.trash) == 2
    assert game.trash.cards[0].name == "Treasure Map"
    assert game.trash.cards[1].name == "Treasure Map"
    assert player.state.actions == 0


def test_treasure_map_throne_room(human: Human, game: Game, monkeypatch):
    responses = ["Treasure Map"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human.hand.add(treasure_map)
    human.hand.add(throne_room)
    assert len(human.deck) == 10

    human.play(throne_room, game)
    assert len(responses) == 0
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Throne Room"
    assert len(human.deck) == 10
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Treasure Map"
    assert human.state.actions == 0
