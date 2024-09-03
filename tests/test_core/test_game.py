import pytest

from pyminion.core import CardType, Card, Supply, Trash
from pyminion.exceptions import InvalidGameSetup, InvalidPlayerCount
from pyminion.expansions.base import (base_set, curse, duchy, estate, gold, province,
                                      smithy, witch)
from pyminion.expansions.alchemy import alchemy_set
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_game_fixture(game: Game):
    assert len(game.players) == 1
    assert isinstance(game.supply, Supply)
    assert isinstance(game.trash, Trash)
    assert not game.trash


def test_game_too_many_players(human: Human):
    with pytest.raises(InvalidPlayerCount):
        Game(players=[human, human, human, human, human], expansions=[])


def test_game_too_few_players():
    with pytest.raises(InvalidPlayerCount):
        Game(players=[], expansions=[])


def test_game_create_supply(game: Game):
    assert len(game.supply.piles) == 17


def test_setup_1_player(human: Human):
    game = Game(players=[human], expansions=[base_set])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 10
    assert game.supply.pile_length(pile_name="Province") == 5
    assert game.supply.pile_length(pile_name="Copper") == 53


def test_setup_2_players(human: Human):
    game = Game(players=[human, human], expansions=[base_set])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 10
    assert game.supply.pile_length(pile_name="Province") == 8
    assert game.supply.pile_length(pile_name="Copper") == 46


def test_setup_3_players(human: Human):
    game = Game(players=[human, human, human], expansions=[base_set])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 20
    assert game.supply.pile_length(pile_name="Province") == 12
    assert game.supply.pile_length(pile_name="Copper") == 39


def test_setup_4_players(human: Human):
    game = Game(players=[human, human, human, human], expansions=[base_set])
    game.supply = game._create_supply()
    assert game.supply.pile_length(pile_name="Curse") == 30
    assert game.supply.pile_length(pile_name="Province") == 12
    assert game.supply.pile_length(pile_name="Copper") == 32


def test_setup_user_selected_card(human):
    game = Game(
        players=[human, human, human, human],
        expansions=[base_set],
        kingdom_cards=[smithy],
    )
    game.supply = game._create_supply()
    assert smithy in game.supply.available_cards()


def test_setup_invalid_user_selected_card(human):
    fake_card = Card(name="fake", cost=0, type=(CardType.Action,))
    game = Game(
        players=[human, human, human, human],
        expansions=[base_set],
        kingdom_cards=[fake_card],
    )
    with pytest.raises(InvalidGameSetup):
        game.supply = game._create_supply()


def test_game_is_over_false(game: Game):
    assert not game.is_over()


def test_game_is_over_true_provinces(game: Game):
    # Single player game ony has 5 provinces
    for _ in range(4):
        game.supply.gain_card(card=province)
    assert not game.is_over()
    game.supply.gain_card(card=province)
    assert game.is_over()


def test_game_is_over_true_three_piles(game: Game):
    for _ in range(5):
        game.supply.gain_card(card=estate)
    assert not game.is_over()
    for _ in range(5):
        game.supply.gain_card(card=duchy)
    assert not game.is_over()
    for _ in range(29):
        game.supply.gain_card(card=gold)
    assert not game.is_over()
    game.supply.gain_card(card=gold)
    assert game.is_over()


def test_game_tie(multiplayer_game: Game):
    # if equal score and equal turns, players tie
    assert multiplayer_game.get_winners() == [
        multiplayer_game.players[0],
        multiplayer_game.players[1],
    ]


def test_game_win(multiplayer_game: Game):
    # player with more points wins
    multiplayer_game.players[0].deck.add(estate)
    assert multiplayer_game.get_winners() == [multiplayer_game.players[0]]


def test_game_win_turns(multiplayer_game: Game):
    # if equal score, player with less turns wins
    multiplayer_game.players[1].turns += 1
    assert multiplayer_game.get_winners() == [multiplayer_game.players[0]]


def test_get_players(decider):
    player1 = Player(decider)
    player2 = Player(decider)
    player3 = Player(decider)

    game2 = Game(players=[player1, player2], expansions=[])
    assert game2.get_left_player(player1) is player2
    assert game2.get_right_player(player1) is player2
    assert game2.get_left_player(player2) is player1
    assert game2.get_right_player(player2) is player1

    game3 = Game(players=[player1, player2, player3], expansions=[])
    assert game3.get_left_player(player1) is player2
    assert game3.get_right_player(player1) is player3
    assert game3.get_left_player(player2) is player3
    assert game3.get_right_player(player2) is player1
    assert game3.get_left_player(player3) is player1
    assert game3.get_right_player(player3) is player2


def test_get_opponents(decider):
    player1 = Player(decider)
    player2 = Player(decider)
    player3 = Player(decider)

    game2 = Game(players=[player1, player2], expansions=[])

    other = list(game2.get_opponents(player1))
    assert len(other) == 1
    assert other[0] is player2

    other = list(game2.get_opponents(player2))
    assert len(other) == 1
    assert other[0] is player1

    game3 = Game(players=[player1, player2, player3], expansions=[])

    other = list(game3.get_opponents(player1))
    assert len(other) == 2
    assert other[0] is player2
    assert other[1] is player3

    other = list(game3.get_opponents(player2))
    assert len(other) == 2
    assert other[0] is player3
    assert other[1] is player1


def test_distribute_curses(decider):
    player21 = Player(decider, player_id='1')
    player22 = Player(decider, player_id='2')
    player41 = Player(decider, player_id='1')
    player42 = Player(decider, player_id='2')
    player43 = Player(decider, player_id='3')
    player44 = Player(decider, player_id='4')

    game2 = Game(
        players=[player21, player22],
        expansions=[base_set],
        random_order=False,
    )
    game2.start()

    game2.distribute_curses(player21, witch)
    assert len(player21.discard_pile) == 0
    assert len(player22.discard_pile) == 1
    assert player22.discard_pile.cards[0].name == "Curse"

    game4 = Game(
        players=[player41, player42, player43, player44],
        expansions=[base_set],
        random_order=False,
    )
    game4.start()
    curse_pile = game4.supply.get_pile("Curse")
    while len(curse_pile) > 2:
        curse_pile.remove(curse)
    assert len(curse_pile) == 2

    game4.distribute_curses(player43, witch)
    assert len(player41.discard_pile) == 1
    assert player41.discard_pile.cards[0].name == "Curse"
    assert len(player42.discard_pile) == 0
    assert len(player43.discard_pile) == 0
    assert len(player44.discard_pile) == 1
    assert player44.discard_pile.cards[0].name == "Curse"


def test_include_potions(decider):
    player1 = Player(decider)
    player2 = Player(decider)

    # game should not have potion when it has no cards with potion in the cost
    game_no_potions = Game(
        players=[player1, player2],
        expansions=[base_set],
        kingdom_cards=base_set[:10],
    )
    game_no_potions.start()
    assert not any(pile.name == "Potion" for pile in game_no_potions.supply.piles)

    # game should have potion when it has cards with potion in the cost
    game_potions = Game(
        players=[player1, player2],
        expansions=[alchemy_set],
        kingdom_cards=alchemy_set[:10],
    )
    game_potions.start()
    assert any(pile.name == "Potion" for pile in game_potions.supply.piles)
