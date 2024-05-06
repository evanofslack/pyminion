from pyminion.core import Action, CardType, Victory, get_action_cards, get_treasure_cards, get_victory_cards, get_score_cards, plural
from pyminion.expansions.base import gold, silver, copper, province, duchy, estate, curse, market, smithy
from pyminion.expansions.intrigue import nobles
from pyminion.game import Game
from pyminion.player import Player

test_action = Action("test", 1, (CardType.Action,))
test_victory = Victory("test", 1, (CardType.Victory,))


def test_plural():
    assert plural("card", 0) == "cards"
    assert plural("card", 1) == "card"
    assert plural("card", 2) == "cards"


def test_get_action_cards():
    cards_in = [
        market,
        gold,
        estate,
        nobles,
        province,
        silver,
        duchy,
        smithy,
        curse,
    ]
    cards_out = list(get_action_cards(cards_in))
    assert len(cards_out) == 3
    assert cards_out[0].name == "Market"
    assert cards_out[1].name == "Nobles"
    assert cards_out[2].name == "Smithy"


def test_get_treasure_cards():
    cards_in = [
        gold,
        estate,
        silver,
        duchy,
        copper,
        smithy,
        estate,
        copper,
        curse,
    ]
    cards_out = list(get_treasure_cards(cards_in))
    assert len(cards_out) == 4
    assert cards_out[0].name == "Gold"
    assert cards_out[1].name == "Silver"
    assert cards_out[2].name == "Copper"
    assert cards_out[3].name == "Copper"


def test_get_victory_cards():
    cards_in = [
        gold,
        estate,
        province,
        silver,
        duchy,
        copper,
        smithy,
        nobles,
        curse,
    ]
    cards_out = list(get_victory_cards(cards_in))
    assert len(cards_out) == 4
    assert cards_out[0].name == "Estate"
    assert cards_out[1].name == "Province"
    assert cards_out[2].name == "Duchy"
    assert cards_out[3].name == "Nobles"


def test_get_score_cards():
    cards_in = [
        gold,
        curse,
        province,
        smithy,
        copper,
        duchy,
        nobles,
    ]
    cards_out = list(get_score_cards(cards_in))
    assert len(cards_out) == 4
    assert cards_out[0].name == "Curse"
    assert cards_out[1].name == "Province"
    assert cards_out[2].name == "Duchy"
    assert cards_out[3].name == "Nobles"


def test_action_card_starting_count(player: Player):
    players = [player] * 2
    game = Game(players, [])

    assert test_action.get_pile_starting_count(game) == 10


def test_victory_card_start_count_2_players(player: Player):
    players = [player] * 2
    game = Game(players, [])

    assert test_victory.get_pile_starting_count(game) == 8


def test_victory_card_start_count_3_players(player: Player):
    players = [player] * 3
    game = Game(players, [])

    assert test_victory.get_pile_starting_count(game) == 12
