from pyminion.expansions.base import silver, gold
from pyminion.expansions.seaside import corsair
from pyminion.game import Game


def test_corsair(multiplayer_game: Game):
    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    p1.hand.add(corsair)

    p1.play(corsair, multiplayer_game)
    assert p1.state.actions == 0
    assert p1.state.money == 2

    p1.start_cleanup_phase(multiplayer_game)
    p1.end_turn(multiplayer_game)

    p2.start_turn(multiplayer_game)

    p2.hand.add(silver)
    p2.hand.add(silver)

    # assert 1st played silver is trashed
    p2.play(silver, multiplayer_game)
    assert p2.state.money == 2
    assert len(p2.playmat) == 0
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Silver"

    # assert 2nd played silver is not trashed
    p2.play(silver, multiplayer_game)
    assert p2.state.money == 4
    assert len(p2.playmat) == 1
    assert p2.playmat.cards[0].name == "Silver"
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Silver"

    p2.end_turn(multiplayer_game)

    assert len(p1.hand) == 5

    p1.start_turn(multiplayer_game)

    assert len(p1.hand) == 6


def test_corsair_unregistered(multiplayer_game: Game):
    # test if corsair trashing effects are unregistered at the start of the
    # playing player's next turn
    p1 = multiplayer_game.players[0]
    p2 = multiplayer_game.players[1]

    # p1 plays corsair
    p1.hand.add(corsair)
    p1.play(corsair, multiplayer_game)
    p1.start_cleanup_phase(multiplayer_game)
    p1.end_turn(multiplayer_game)

    # p2 does not play silver or gold on their turn
    p2.start_turn(multiplayer_game)
    p2.start_cleanup_phase(multiplayer_game)
    p2.end_turn(multiplayer_game)

    # p1 takes their next turn (corsair trashing effect should end)
    p1.start_turn(multiplayer_game)
    p1.start_cleanup_phase(multiplayer_game)
    p1.end_turn(multiplayer_game)

    # p2 takes their next turn and should not have to trash silver or gold
    p2.start_turn(multiplayer_game)
    p2.hand.add(gold)
    p2.play(gold, multiplayer_game)
    assert p2.state.money == 3
    assert len(p2.playmat) == 1
    assert p2.playmat.cards[0].name == "Gold"
    assert len(multiplayer_game.trash) == 0


def test_corsair_multiple(multiplayer4_game: Game):
    p1 = multiplayer4_game.players[0]
    p2 = multiplayer4_game.players[1]
    p3 = multiplayer4_game.players[2]
    p4 = multiplayer4_game.players[3]

    # p1's turn: play corsair
    p1.start_turn(multiplayer4_game)
    p1.hand.add(corsair)
    p1.play(corsair, multiplayer4_game)
    p1.start_cleanup_phase(multiplayer4_game)
    p1.end_turn(multiplayer4_game)

    # p2's turn: play corsair
    p2.start_turn(multiplayer4_game)
    p2.hand.add(corsair)
    p2.play(corsair, multiplayer4_game)
    p2.start_cleanup_phase(multiplayer4_game)
    p2.end_turn(multiplayer4_game)

    # p3's turn: play golds, should only trash 1
    p3.start_turn(multiplayer4_game)
    p3.hand.add(gold)
    p3.hand.add(gold)
    p3.play(gold, multiplayer4_game)
    assert p3.state.money == 3
    assert len(p3.playmat) == 0
    assert len(multiplayer4_game.trash) == 1
    assert multiplayer4_game.trash.cards[0].name == "Gold"
    p3.play(gold, multiplayer4_game)
    assert p3.state.money == 6
    assert len(p3.playmat) == 1
    assert p3.playmat.cards[0].name == "Gold"
    assert len(multiplayer4_game.trash) == 1
    assert multiplayer4_game.trash.cards[0].name == "Gold"
