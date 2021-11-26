from pyminion.bots import OptimizedBot
from pyminion.expansions.base import (
    Silver,
    copper,
    duchy,
    estate,
    gold,
    harbinger,
    province,
    silver,
)
from pyminion.game import Game
from pyminion.players import Human


def test_harbinger_valid_topdeck(human: Human, game: Game, monkeypatch):
    human.hand.add(harbinger)
    human.discard_pile.add(silver)

    monkeypatch.setattr("builtins.input", lambda _: "Silver")

    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert type(human.deck.cards[-1]) is Silver


def test_harbinger_bot_no_topdeck_victory(bot: OptimizedBot, game: Game):
    bot.hand.add(harbinger)
    bot.discard_pile.add(estate)
    bot.discard_pile.add(duchy)
    bot.discard_pile.add(province)
    bot.discard_pile.add(copper)
    bot.play(harbinger, game)
    assert len(bot.discard_pile) == 4


def test_harbinger_bot_topdeck_expensive_card(bot: OptimizedBot, game: Game):
    bot.hand.add(harbinger)
    bot.discard_pile.add(silver)
    bot.discard_pile.add(gold)  # Topdeck me
    bot.discard_pile.add(province)
    bot.play(harbinger, game)
    assert len(bot.discard_pile) == 2
    assert bot.deck.cards[-1].name == "Gold"
