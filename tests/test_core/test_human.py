from pyminion.players import Human


def test_human_start_turn(human: Human):
    assert human.turns == 0
    human.start_turn()
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.state.buys == 1
    assert human.turns == 1


def test_human_cleanup(human: Human):
    human.draw(5)
    assert len(human.hand) == 5
    assert len(human.discard_pile) == 0
    assert len(human.playmat) == 0
    human.start_cleanup_phase()
    assert len(human.discard_pile) == 5
    assert len(human.hand) == 5
    assert len(human.playmat) == 0
