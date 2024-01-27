from pyminion.expansions.base import merchant, throne_room, silver
from pyminion.human import Human
from pyminion.game import Game
from pyminion.expansions.base import Merchant
from pyminion.player import Player


def test_merchant_no_silver(player: Player, game: Game):
    player.hand.add(merchant)
    assert len(player.hand) == 1
    player.play(merchant, game)
    assert len(player.hand) == 1
    assert len(player.playmat) == 1
    assert type(player.playmat.cards[0]) is Merchant
    assert player.state.actions == 1
    assert player.state.money == 0
    assert player.state.buys == 1


def test_merchant_one_silver(player: Player, game: Game):
    player.hand.add(merchant)
    player.hand.add(silver)
    assert len(player.hand) == 2
    player.play(target_card=merchant, game=game)
    player.play(target_card=silver, game=game)

    assert len(player.hand) == 1
    assert len(player.playmat) == 2
    assert type(player.playmat.cards[0]) is Merchant
    assert player.state.actions == 1
    assert player.state.money == 3
    assert player.state.buys == 1


def test_hand_merchant(player: Player, game: Game):
    # only play one merchant and make sure merchant in hand is not counted
    player.hand.add(merchant)
    player.hand.add(merchant)
    player.hand.add(silver)
    assert len(player.hand) == 3
    player.play(target_card=merchant, game=game)
    player.play(target_card=silver, game=game)

    assert len(player.hand) == 2
    assert len(player.playmat) == 2
    assert type(player.playmat.cards[0]) is Merchant
    assert player.state.actions == 1
    assert player.state.money == 3
    assert player.state.buys == 1


def test_merchant_two_silvers(player: Player, game: Game):
    player.hand.add(merchant)
    player.hand.add(silver)
    player.hand.add(silver)
    assert len(player.hand) == 3
    player.play(target_card=merchant, game=game)
    player.play(target_card=silver, game=game)
    player.play(target_card=silver, game=game)

    assert len(player.hand) == 1
    assert len(player.playmat) == 3
    assert player.state.actions == 1
    assert player.state.money == 5
    assert player.state.buys == 1


def test_two_merchants_one_silver(player: Player, game: Game):
    player.hand.add(merchant)
    player.hand.add(merchant)
    player.hand.add(silver)
    assert len(player.hand) == 3
    player.play(target_card=merchant, game=game)
    player.play(target_card=merchant, game=game)
    player.play(target_card=silver, game=game)

    assert len(player.hand) == 2
    assert len(player.playmat) == 3
    assert player.state.actions == 1
    assert player.state.money == 4
    assert player.state.buys == 1


def test_two_merchants_two_silvers(player: Player, game: Game):
    player.hand.add(merchant)
    player.hand.add(merchant)
    player.hand.add(silver)
    player.hand.add(silver)
    assert len(player.hand) == 4
    player.play(target_card=merchant, game=game)
    player.play(target_card=merchant, game=game)
    player.play(target_card=silver, game=game)
    player.play(target_card=silver, game=game)

    assert len(player.hand) == 2
    assert len(player.playmat) == 4
    assert player.state.actions == 1
    assert player.state.money == 6
    assert player.state.buys == 1


def test_merchant_throne_room(human: Human, game: Game, monkeypatch):
    human.hand.add(throne_room)
    human.hand.add(merchant)
    human.hand.add(silver)
    human.hand.add(silver)

    monkeypatch.setattr("builtins.input", lambda _: "Merchant")

    human.play(throne_room, game)
    human.play(silver, game)
    human.play(silver, game)

    assert len(human.hand) == 2
    assert len(human.playmat) == 4
    assert human.state.actions == 2
    assert human.state.money == 6
    assert human.state.buys == 1


def test_merchant_reset(player: Player, game: Game):
    player.hand.add(merchant)
    player.hand.add(silver)
    assert len(player.hand) == 2
    player.play(target_card=merchant, game=game)
    player.play(target_card=silver, game=game)

    assert len(player.hand) == 1
    assert len(player.playmat) == 2
    assert type(player.playmat.cards[0]) is Merchant
    assert player.state.actions == 1
    assert player.state.money == 3
    assert player.state.buys == 1

    player.start_cleanup_phase(game)
    game.effect_registry.on_turn_end(player, game)

    player.hand.add(silver)
    player.play(silver, game)
    assert player.state.money == 2
