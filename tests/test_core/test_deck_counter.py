from pyminion.core import Deck, DeckCounter
from pyminion.expansions.base import base_set, copper, estate
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player


def test_deck_counter_no_args():
    deck_counter = DeckCounter()
    assert str(deck_counter) == ""


def test_deck_counter_empty():
    deck = Deck()
    deck_counter = DeckCounter(deck.cards)
    assert str(deck_counter) == ""


def test_deck_counter_starting_cards():
    players: list[Player] = [Human(player_id=f"human{i}") for i in range(2)]
    game = Game(players, [base_set])
    game.start()
    player1 = game.players[0]

    deck_counter1 = DeckCounter(player1.get_all_cards())
    assert str(deck_counter1) in ["7 Copper, 3 Estate", "3 Estate, 7 Copper"]

    player1.gain(copper, game)
    player1.gain(estate, game)

    deck_counter2 = DeckCounter(player1.get_all_cards())
    assert str(deck_counter2) in ["8 Copper, 4 Estate", "4 Estate, 8 Copper"]
