from pyminion.bots.bot import Bot
from pyminion.core import Card
from pyminion.effects import PlayerGameEffect
from pyminion.expansions.base import copper, estate, gold, witch
from pyminion.game import Game
import pytest


def test_effects_order_decision(base_bot: Bot, game: Game):
    effect = PlayerGameEffect("test")
    assert base_bot.decider.effects_order_decision([effect], base_bot, game) == 0


def test_binary_decision(base_bot: Bot, game: Game):
    assert base_bot.decider.binary_decision(prompt="test", card=copper, player=base_bot, game=game, relevant_cards=None)


def test_multiple_option_decision(base_bot: Bot, game: Game):
    decision = base_bot.decider.multiple_option_decision(
        copper,
        ["A", "B", "C"],
        base_bot,
        game,
        num_choices=2,
    )
    assert decision == [0, 1]


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


def test_topdeck_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.topdeck_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_topdeck=1,
    )
    assert len(cards) == 1
    assert cards[0].name == "Copper"


def test_topdeck_decision_none(base_bot: Bot, game: Game):
    cards = base_bot.decider.topdeck_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        min_num_topdeck=0,
    )
    assert len(cards) == 0


def test_deck_position_decision(base_bot: Bot, game: Game):
    position = base_bot.decider.deck_position_decision(
        "",
        copper,
        base_bot,
        game,
        num_deck_cards=5,
    )
    assert position == 5


def test_reveal_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.reveal_decision(
        "",
        copper,
        [copper, estate, gold],
        base_bot,
        game,
        min_num_reveal=2,
        max_num_reveal=3,
    )
    assert len(cards) == 2
    assert cards[0].name == "Copper"
    assert cards[1].name == "Estate"


def test_pass_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.pass_decision(
        "",
        copper,
        [copper, estate, gold],
        base_bot,
        game,
        min_num_pass=2,
        max_num_pass=3,
    )
    assert len(cards) == 2
    assert cards[0].name == "Copper"
    assert cards[1].name == "Estate"


def test_name_card_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.name_card_decision(
        "",
        copper,
        [copper, estate, gold],
        base_bot,
        game,
        min_num_name=2,
        max_num_name=3,
    )
    assert len(cards) == 2
    assert cards[0].name == "Copper"
    assert cards[1].name == "Estate"


def test_multi_play_decision(base_bot: Bot, game: Game):
    card = base_bot.decider.multi_play_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        required=True,
    )
    assert card is not None
    assert card.name == "Copper"


def test_multi_play_decision_none(base_bot: Bot, game: Game):
    card = base_bot.decider.multi_play_decision(
        prompt="",
        card=copper,
        valid_cards=[copper, estate, gold],
        player=base_bot,
        game=game,
        required=False,
    )
    assert card is None


def test_set_aside_decision(base_bot: Bot, game: Game):
    cards = base_bot.decider.set_aside_decision(
        "",
        copper,
        [copper, estate, gold],
        base_bot,
        game,
        min_num_set_aside=2,
        max_num_set_aside=3,
    )
    assert len(cards) == 2
    assert cards[0].name == "Copper"
    assert cards[1].name == "Estate"


def test_is_attacked(base_bot: Bot, game: Game):
    assert base_bot.is_attacked(attacking_player=base_bot, attack_card=witch, game=game)


def test_action_decision(base_bot: Bot, game: Game):
    with pytest.raises(NotImplementedError):
        base_bot.decider.action_phase_decision([], base_bot, game)


def test_treasure_decision(base_bot: Bot, game: Game):
    treasures: list[Card] = [copper, gold]
    cards = base_bot.decider.treasure_phase_decision(treasures, base_bot, game)
    assert len(cards) == 2
    assert treasures[0] == copper
    assert treasures[1] == gold


def test_buy_decision(base_bot: Bot, game: Game):
    with pytest.raises(NotImplementedError):
        base_bot.decider.buy_phase_decision([], base_bot, game)
