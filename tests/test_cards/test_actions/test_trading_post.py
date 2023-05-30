from pyminion.expansions.base import copper, duchy, estate
from pyminion.expansions.intrigue import TradingPost, trading_post
from pyminion.game import Game
from pyminion.human import Human


def test_trading_post_no_cards(human: Human, game: Game):
    human.hand.add(trading_post)

    human.play(trading_post, game)
    assert len(human.hand) == 0
    assert len(game.trash) == 0
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TradingPost
    assert human.state.actions == 0


def test_trading_post_1_card(human: Human, game: Game):
    human.hand.add(trading_post)
    human.hand.add(copper)

    human.play(trading_post, game)
    assert len(human.hand) == 0
    assert len(game.trash) == 1
    assert game.trash.cards[0].name == "Copper"
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TradingPost
    assert human.state.actions == 0


def test_trading_post_2_cards(human: Human, game: Game):
    human.hand.add(trading_post)
    human.hand.add(copper)
    human.hand.add(estate)

    human.play(trading_post, game)
    assert len(human.hand) == 1
    assert human.hand.cards[0].name == "Silver"
    assert len(game.trash) == 2
    trash_card_names = [c.name for c in game.trash.cards]
    assert "Copper" in trash_card_names
    assert "Estate" in trash_card_names
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TradingPost
    assert human.state.actions == 0


def test_trading_post_3_cards(human: Human, game: Game, monkeypatch):
    human.hand.add(trading_post)
    human.hand.add(copper)
    human.hand.add(duchy)
    human.hand.add(estate)

    responses = iter(["copper, estate"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    human.play(trading_post, game)
    assert len(human.hand) == 2
    hand_card_names = [c.name for c in human.hand.cards]
    assert "Duchy" in hand_card_names
    assert "Silver" in hand_card_names
    assert len(game.trash) == 2
    trash_card_names = [c.name for c in game.trash.cards]
    assert "Copper" in trash_card_names
    assert "Estate" in trash_card_names
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is TradingPost
    assert human.state.actions == 0
