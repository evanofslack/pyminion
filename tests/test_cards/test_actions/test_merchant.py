from pyminion.expansions.base import merchant, silver
from pyminion.game import Game
from pyminion.expansions.base import Merchant
from pyminion.human import Human


def test_merchant_no_silver(human: Human, game: Game):
    human.hand.add(merchant)
    assert len(human.hand) == 1
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Merchant
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.state.buys == 1


def test_merchant_one_silver(human: Human, game: Game):
    human.hand.add(merchant)
    human.hand.add(silver)
    assert len(human.hand) == 2
    # human.hand.cards[0].play(human, game)
    human.play(target_card=merchant, game=game)
    human.play(target_card=silver, game=game)

    assert len(human.hand) == 1
    assert len(human.playmat) == 2
    assert type(human.playmat.cards[0]) is Merchant
    assert human.state.actions == 1
    assert human.state.money == 3
    assert human.state.buys == 1


def test_merchant_two_silvers(human: Human, game: Game):
    human.hand.add(merchant)
    human.hand.add(silver)
    human.hand.add(silver)
    assert len(human.hand) == 3
    human.play(target_card=merchant, game=game)
    human.play(target_card=silver, game=game)
    human.play(target_card=silver, game=game)

    assert len(human.hand) == 1
    assert len(human.playmat) == 3
    assert human.state.actions == 1
    assert human.state.money == 5
    assert human.state.buys == 1


def test_two_merchants_one_silver(human: Human, game: Game):
    human.hand.add(merchant)
    human.hand.add(merchant)
    human.hand.add(silver)
    assert len(human.hand) == 3
    human.play(target_card=merchant, game=game)
    human.play(target_card=merchant, game=game)
    human.play(target_card=silver, game=game)

    assert len(human.hand) == 2
    assert len(human.playmat) == 3
    assert human.state.actions == 1
    assert human.state.money == 4
    assert human.state.buys == 1


def test_two_merchants_two_silvers(human: Human, game: Game):
    human.hand.add(merchant)
    human.hand.add(merchant)
    human.hand.add(silver)
    human.hand.add(silver)
    assert len(human.hand) == 4
    human.play(target_card=merchant, game=game)
    human.play(target_card=merchant, game=game)
    human.play(target_card=silver, game=game)
    human.play(target_card=silver, game=game)

    assert len(human.hand) == 2
    assert len(human.playmat) == 4
    assert human.state.actions == 1
    assert human.state.money == 6
    assert human.state.buys == 1
