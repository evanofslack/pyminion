from pyminion.bots import OptimizedBot
from pyminion.expansions.base import copper, gold, mine, silver
from pyminion.game import Game
from pyminion.players import Human


def test_mine_no_treasures(human: Human, game: Game, monkeypatch):
    human.hand.add(mine)
    human.play(mine, game)
    assert len(game.trash) == 0


def test_mine_gain_valid(human: Human, game: Game, monkeypatch):
    human.hand.add(copper)
    human.hand.add(mine)
    assert len(game.trash) == 0

    responses = iter(["copper", "silver"])
    monkeypatch.setattr("builtins.input", lambda input: next(responses))

    human.play(mine, game)
    assert len(human.playmat) == 1
    assert human.state.actions == 0
    assert game.trash.cards[0].name == "Copper"
    assert human.hand.cards[-1].name == "Silver"


def test_mine_bot_no_treasure(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.play(mine, game)
    assert len(game.trash) == 0


def test_mine_bot_copper(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.hand.add(copper)
    bot.play(mine, game)
    assert bot.hand.cards[-1].name == "Silver"


def test_mine_bot_silver(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.hand.add(silver)
    bot.play(mine, game)
    assert bot.hand.cards[-1].name == "Gold"


def test_mine_bot_gold(bot: OptimizedBot, game: Game):
    bot.hand.add(mine)
    bot.hand.add(gold)
    bot.play(mine, game)
    assert bot.hand.cards[-1].name == "Gold"
