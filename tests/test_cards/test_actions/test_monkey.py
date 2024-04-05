from pyminion.core import DeckCounter
from pyminion.expansions.base import copper
from pyminion.expansions.seaside import Monkey, monkey
from pyminion.game import Game
from pyminion.player import Player


def test_monkey_no_gain(player: Player, game: Game):
    for _ in range(5):
        player.deck.add(copper)
    player.hand.add(monkey)

    player.play(monkey, game)
    assert len(player.hand) == 0
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Monkey
    assert len(player.discard_pile) == 0
    assert player.state.actions == 0
    assert player.playmat_persist_counts[monkey.name] == 1

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Monkey
    assert len(player.discard_pile) == 0
    assert player.playmat_persist_counts[monkey.name] == 1

    player.start_turn(game)

    assert len(player.hand) == 6
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Monkey
    assert len(player.discard_pile) == 0
    assert player.playmat_persist_counts[monkey.name] == 0

    player.start_cleanup_phase(game)

    assert len(player.hand) == 5
    assert len(player.playmat) == 0
    counter = DeckCounter(player.discard_pile.cards)
    assert counter[monkey] == 1
    assert player.playmat_persist_counts[monkey.name] == 0


def test_monkey_gain(multiplayer_game: Game):
    player1 = multiplayer_game.players[0]
    player2 = multiplayer_game.players[1]

    for _ in range(5):
        player1.deck.add(copper)
    player1.hand.add(monkey)
    player1.play(monkey, multiplayer_game)
    assert player1.state.actions == 0

    player1.start_cleanup_phase(multiplayer_game)
    assert len(player1.hand) == 5

    player2.start_turn(multiplayer_game)

    player2.gain(copper, multiplayer_game)
    assert len(player1.hand) == 6

    player2.gain(copper, multiplayer_game)
    assert len(player1.hand) == 7

    player2.start_cleanup_phase(multiplayer_game)
    player2.end_turn(multiplayer_game)

    player1.start_turn(multiplayer_game)
    assert len(player1.hand) == 8
