from pyminion.bots import Bot
from pyminion.expansions.base import copper, moat
from pyminion.game import Game


def test_bot_play(bot: Bot, game: Game):
    bot.hand.add(moat)
    bot.play(moat, game)
    assert bot.playmat.cards[0].name == "Moat"
