from typing import List, Optional
import pytest
from pyminion.bots.bot import Bot
from pyminion.bots.examples import BigMoney
from pyminion.bots.optimized_bot import OptimizedBot
from pyminion.core import Deck, Pile, Supply, Trash
from pyminion.expansions.base import (
    base_set,
    copper,
    duchy,
    estate,
    gold,
    province,
    silver,
    smithy,
)
from pyminion.expansions.intrigue import (
    intrigue_set,
    mill,
)
from pyminion.game import Game, Card
from pyminion.human import Human
from pyminion.player import Player

START_COPPER = 7
START_ESTATE = 3


class TestDecider:
    def binary_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List["Card"]] = None,
    ) -> bool:
        return True


@pytest.fixture
def decider():
    decider = TestDecider()
    return decider


@pytest.fixture
def deck():
    start_cards = [copper] * START_COPPER + [estate] * START_ESTATE
    deck = Deck(cards=start_cards)
    return deck


@pytest.fixture
def player(decider, deck):
    player = Player(decider=decider, deck=deck, player_id="test")
    return player


@pytest.fixture
def human(deck):
    human = Human(deck=deck, player_id="human")
    return human


@pytest.fixture
def bot(deck):
    bot = OptimizedBot(player_id="bot")
    bot.deck = deck
    return bot


@pytest.fixture
def bm_bot(deck):
    bot = BigMoney(player_id="bot")
    bot.deck = deck
    return bot


@pytest.fixture
def base_bot(deck):
    bot = Bot(player_id="bot")
    bot.deck = deck
    return bot


@pytest.fixture
def trash():
    trash = Trash()
    return trash


@pytest.fixture
def supply():
    estates = Pile([estate] * 8)
    duchies = Pile([duchy] * 8)
    provinces = Pile([province] * 8)
    coppers = Pile([copper] * 60)
    silvers = Pile([silver] * 40)
    golds = Pile([gold] * 30)
    supply = Supply([estates, duchies, provinces, coppers, silvers, golds])
    return supply


@pytest.fixture
def game(player):
    game = Game(
        players=[player],
        expansions=[base_set, intrigue_set],
        kingdom_cards=[mill, smithy],
        # start_cards=start_cards,
    )
    game.supply = game._create_supply()
    return game


@pytest.fixture
def multiplayer_game():

    human1 = Human(player_id="human_1")
    human2 = Human(player_id="human_2")

    game = Game(
        players=[human1, human2],
        expansions=[base_set, intrigue_set],
        kingdom_cards=[mill, smithy],
    )
    game.start()

    return game


@pytest.fixture
def multiplayer_bot_game():

    bot1 = OptimizedBot(player_id="bot_1")
    bot2 = OptimizedBot(player_id="bot_2")

    game = Game(
        players=[bot1, bot2],
        expansions=[base_set],
    )
    game.start()

    return game
