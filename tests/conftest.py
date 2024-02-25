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
)
from pyminion.expansions.intrigue import (
    intrigue_set,
)
from pyminion.game import Game, Card
from pyminion.human import Human
from pyminion.player import Player

START_COPPER = 7
START_ESTATE = 3


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "kingdom_cards(cards): kingdom cards for game"
    )


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
    copper_cards: List["Card"] = [copper] * START_COPPER
    estate_cards: List["Card"] = [estate] * START_ESTATE
    start_cards: List["Card"] = copper_cards + estate_cards

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
    estate_cards: List["Card"] = [estate] * 8
    estates = Pile(estate_cards)
    duchy_cards: List["Card"] = [duchy] * 8
    duchies = Pile(duchy_cards)
    province_cards: List["Card"] = [province] * 8
    provinces = Pile(province_cards)
    copper_cards: List["Card"] = [copper] * 60
    coppers = Pile(copper_cards)
    silver_cards: List["Card"] = [silver] * 40
    silvers = Pile(silver_cards)
    gold_cards: List["Card"] = [gold] * 30
    golds = Pile(gold_cards)
    supply = Supply([estates, duchies, provinces, coppers, silvers, golds])
    return supply


@pytest.fixture
def game(request, player):
    marker = request.node.get_closest_marker("kingdom_cards")
    if marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = marker.args[0]

    game = Game(
        players=[player],
        expansions=[base_set, intrigue_set],
        kingdom_cards=kingdom_cards,
    )
    game.supply = game._create_supply()
    for card in game.all_game_cards:
        card.set_up(game)
    return game


@pytest.fixture
def multiplayer_game(request):
    marker = request.node.get_closest_marker("kingdom_cards")
    if marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = marker.args[0]

    human1 = Human(player_id="human_1")
    human2 = Human(player_id="human_2")

    game = Game(
        players=[human1, human2],
        expansions=[base_set, intrigue_set],
        kingdom_cards=kingdom_cards,
    )
    game.start()

    return game


@pytest.fixture
def multiplayer_bot_game(request):
    marker = request.node.get_closest_marker("kingdom_cards")
    if marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = marker.args[0]

    bot1 = OptimizedBot(player_id="bot_1")
    bot2 = OptimizedBot(player_id="bot_2")

    game = Game(
        players=[bot1, bot2],
        expansions=[base_set, intrigue_set],
        kingdom_cards=kingdom_cards,
    )
    game.start()

    return game
