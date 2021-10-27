import pytest

from pyminion.expansions.base import copper, silver, gold, estate, duchy, province
from pyminion.models.core import (
    Pile,
    Deck,
    Player,
    Supply,
    Trash,
    Game,
)
from pyminion.expansions.base import start_cards

START_COPPER = 7
START_ESTATE = 3


@pytest.fixture
def deck():
    start_cards = [copper] * START_COPPER + [estate] * START_ESTATE
    deck = Deck(cards=start_cards)
    return deck


@pytest.fixture
def player(deck):
    player = Player(
        deck=deck,
        player_id="test",
    )
    return player


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
def game(player, supply, trash):
    game = Game(players=[player], supply=supply, trash=trash)
    return game


@pytest.fixture
def multiplayer_game(player, supply, trash):

    player2 = Player(
        deck=Deck(start_cards),
        player_id="Test_2",
    )

    game = Game(players=[player, player2], supply=supply, trash=trash)
    return game
