import pytest
from pyminion.bots.bot import Bot
from pyminion.bots.examples import BigMoney
from pyminion.bots.optimized_bot import OptimizedBot
from pyminion.core import Deck, Pile, Supply, Trash
from pyminion.effects import EffectRegistry
from pyminion.expansions.base import (
    base_set,
    copper,
    duchy,
    estate,
    gold,
    province,
    silver,
)
from pyminion.game import Game, Card
from pyminion.human import Human
from pyminion.player import Player

START_COPPER = 7
START_ESTATE = 3


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "expansions(expansions): expansions for game"
    )
    config.addinivalue_line(
        "markers", "kingdom_cards(cards): kingdom cards for game"
    )


class TestDecider:
    def buy_phase_decision(
        self,
        valid_cards: list[Card],
        player: "Player",
        game: "Game",
    ) -> Card|None:
        return None

    def binary_decision(
        self,
        prompt: str,
        card: "Card",
        player: "Player",
        game: "Game",
        relevant_cards: list[Card]|None = None,
    ) -> bool:
        return True


@pytest.fixture
def decider():
    decider = TestDecider()
    return decider


@pytest.fixture
def deck():
    copper_cards: list[Card] = [copper] * START_COPPER
    estate_cards: list[Card] = [estate] * START_ESTATE
    start_cards: list[Card] = copper_cards + estate_cards

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
    estate_cards: list[Card] = [estate] * 8
    estates = Pile(estate_cards)
    duchy_cards: list[Card] = [duchy] * 8
    duchies = Pile(duchy_cards)
    province_cards: list[Card] = [province] * 8
    provinces = Pile(province_cards)
    copper_cards: list[Card] = [copper] * 60
    coppers = Pile(copper_cards)
    silver_cards: list[Card] = [silver] * 40
    silvers = Pile(silver_cards)
    gold_cards: list[Card] = [gold] * 30
    golds = Pile(gold_cards)
    supply = Supply([estates, duchies, provinces], [coppers, silvers, golds], [])
    return supply


@pytest.fixture
def effect_registry():
    effect_registry = EffectRegistry()
    return effect_registry


@pytest.fixture
def game(request, player):
    expansions_marker = request.node.get_closest_marker("expansions")
    if expansions_marker is None:
        expansions = [base_set]
    else:
        expansions = expansions_marker.args[0]

    kingdom_cards_marker = request.node.get_closest_marker("kingdom_cards")
    if kingdom_cards_marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = kingdom_cards_marker.args[0]

    game = Game(
        players=[player],
        expansions=expansions,
        kingdom_cards=kingdom_cards,
    )

    # TODO: It would be better to call game.start() here, but this breaks
    # several unit tests, so they need to be fixed first
    game.supply = game._create_supply()
    for card in game.all_game_cards:
        card.set_up(game)
    player.hand.on_add = lambda card, player=player: game.effect_registry.on_hand_add(player, card, game)
    player.hand.on_remove = lambda card, player=player: game.effect_registry.on_hand_remove(player, card, game)
    player.deck.on_shuffle = lambda player=player: game.effect_registry.on_shuffle(player, game)

    return game


@pytest.fixture
def multiplayer_game(request):
    expansions_marker = request.node.get_closest_marker("expansions")
    if expansions_marker is None:
        expansions = [base_set]
    else:
        expansions = expansions_marker.args[0]

    marker = request.node.get_closest_marker("kingdom_cards")
    if marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = marker.args[0]

    human1 = Human(player_id="human_1")
    human2 = Human(player_id="human_2")

    game = Game(
        players=[human1, human2],
        expansions=expansions,
        kingdom_cards=kingdom_cards,
    )
    game.start()

    return game


@pytest.fixture
def multiplayer4_game(request):
    expansions_marker = request.node.get_closest_marker("expansions")
    if expansions_marker is None:
        expansions = [base_set]
    else:
        expansions = expansions_marker.args[0]

    marker = request.node.get_closest_marker("kingdom_cards")
    if marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = marker.args[0]

    human1 = Human(player_id="human_1")
    human2 = Human(player_id="human_2")
    human3 = Human(player_id="human_3")
    human4 = Human(player_id="human_4")

    game = Game(
        players=[human1, human2, human3, human4],
        expansions=expansions,
        kingdom_cards=kingdom_cards,
    )
    game.start()

    return game


@pytest.fixture
def multiplayer_bot_game(request):
    expansions_marker = request.node.get_closest_marker("expansions")
    if expansions_marker is None:
        expansions = [base_set]
    else:
        expansions = expansions_marker.args[0]

    marker = request.node.get_closest_marker("kingdom_cards")
    if marker is None:
        kingdom_cards = []
    else:
        kingdom_cards = marker.args[0]

    bot1 = OptimizedBot(player_id="bot_1")
    bot2 = OptimizedBot(player_id="bot_2")

    game = Game(
        players=[bot1, bot2],
        expansions=expansions,
        kingdom_cards=kingdom_cards,
    )
    game.start()

    return game
