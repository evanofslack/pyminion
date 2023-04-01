import pytest

from pyminion.bots.bot import Bot
from pyminion.expansions.base import copper, estate, gold, witch
from pyminion.game import Game


def test_binary_decision(base_bot: Bot, game: Game):
    assert base_bot.decider.binary_decision(prompt="test", card=copper, player=base_bot, game=game, relevant_cards=None)


def test_multiple_discard_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.discard_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_discard=2,
        max_num_discard=2,
    )
    assert len(cards) == 2


def test_multiple_discard_decision_none(base_bot: Bot, game: Game):
    cards = base_bot.decider.discard_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        max_num_discard=2,
    )
    assert len(cards) == 0


def test_gain_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.gain_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_gain=1,
    )
    assert len(cards) == 1
    assert cards[0].name == "Copper"


def test_gain_decision_none(base_bot: Bot, game: Game):
    cards = base_bot.decider.gain_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_gain=0,
    )
    assert len(cards) == 0


def test_trash_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.trash_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_trash=1,
    )
    assert len(cards) == 1
    assert cards[0].name == "Copper"


def test_trash_decision_none(base_bot: Bot, game: Game):
    cards = base_bot.decider.trash_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_trash=0,
    )
    assert len(cards) == 0


def test_topdeck_resp(base_bot: Bot, game: Game):
    card = base_bot.topdeck_resp(
        card=None, valid_cards=[copper, estate, gold], game=game, required=True
    )
    assert card.name == "Copper"


def test_topdeck_resp_none(base_bot: Bot, game: Game):
    card = base_bot.topdeck_resp(
        card=None, valid_cards=[copper, estate, gold], game=game, required=False
    )
    assert card is None


def test_double_play_resp(base_bot: Bot, game: Game):
    card = base_bot.double_play_resp(
        card=None, valid_cards=[copper, estate, gold], game=game, required=True
    )
    assert card.name == "Copper"


def test_double_play_resp_none(base_bot: Bot, game: Game):
    card = base_bot.double_play_resp(
        card=None, valid_cards=[copper, estate, gold], game=game, required=False
    )
    assert card is None


def test_is_attacked(base_bot: Bot, game: Game):
    assert base_bot.is_attacked(player=base_bot, attack_card=witch, game=game)


def test_action_priority(base_bot: Bot, game: Game):
    with pytest.raises(NotImplementedError):
        base_bot.action_priority(game)


def test_buy_priority(base_bot: Bot, game: Game):
    with pytest.raises(NotImplementedError):
        base_bot.buy_priority(game)
