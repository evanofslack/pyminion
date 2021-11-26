from pyminion.bots import OptimizedBot
from pyminion.expansions.base import copper, duchy, estate, poacher
from pyminion.game import Game
from pyminion.players import Human


def test_poacher_no_empty_pile(human: Human, game: Game):
    human.hand.add(poacher)
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 0
    assert human.state.actions == 1
    assert human.state.money == 1


def test_poacher_one_empty_pile(human: Human, game: Game, monkeypatch):
    # Single player game only has 5 of each victory card
    for i in range(5):
        game.supply.gain_card(card=estate)
    assert game.supply.num_empty_piles() == 1
    human.hand.add(poacher)
    human.hand.add(estate)
    monkeypatch.setattr("builtins.input", lambda _: "estate")
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 1
    assert human.state.money == 1


def test_poacher_two_empty_piles(human: Human, game: Game, monkeypatch):
    for i in range(5):
        game.supply.gain_card(card=estate)
    for i in range(5):
        game.supply.gain_card(card=duchy)
    assert game.supply.num_empty_piles() == 2
    human.hand.add(poacher)
    human.hand.add(estate)
    assert len(human.hand) == 2
    monkeypatch.setattr("builtins.input", lambda _: "estate, estate")
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 2
    assert human.state.actions == 1
    assert human.state.money == 1


def test_poacher_two_empty_piles_one_in_hand(human: Human, game: Game, monkeypatch):
    for i in range(5):
        game.supply.gain_card(card=estate)
    for i in range(5):
        game.supply.gain_card(card=duchy)
    assert game.supply.num_empty_piles() == 2
    human.hand.add(poacher)
    assert len(human.hand) == 1
    monkeypatch.setattr("builtins.input", lambda _: "estate")
    human.hand.cards[0].play(human, game)
    assert len(human.hand) == 0
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 1
    assert human.state.money == 1


def test_poacher_bot_no_empty_pile(bot: OptimizedBot, game: Game):
    bot.hand.add(poacher)
    bot.play(poacher, game)
    assert len(bot.discard_pile) == 0


def test_bot_one_empty_pile(bot: OptimizedBot, game: Game):
    bot.hand.add(poacher)
    bot.hand.add(estate)
    for i in range(5):
        game.supply.gain_card(card=estate)
    assert game.supply.num_empty_piles() == 1
    bot.play(poacher, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Estate"


def test_bot_one_empty_pile_prioritize_victory(bot: OptimizedBot, game: Game):
    bot.hand.add(poacher)
    bot.hand.add(estate)
    bot.hand.add(copper)
    for i in range(5):
        game.supply.gain_card(card=estate)
    assert game.supply.num_empty_piles() == 1
    bot.play(poacher, game)
    assert len(bot.discard_pile) == 1
    assert bot.discard_pile.cards[-1].name == "Estate"
