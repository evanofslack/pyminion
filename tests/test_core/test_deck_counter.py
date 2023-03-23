from pyminion.core import Deck, DeckCounter
from pyminion.expansions.base import base_set, copper, estate
from pyminion.game import Game
from pyminion.players import Human, Player
from typing import List


def test_deck_counter_no_args():
    deck_counter = DeckCounter()
    assert str(deck_counter) == ""


def test_deck_counter_empty():
    deck = Deck()
    deck_counter = DeckCounter(deck.cards)
    assert str(deck_counter) == ""


def test_deck_counter_starting_cards():
    players: List[Player] = [Human(player_id=f"human{i}") for i in range(2)]
    game = Game(players, [base_set])
    game.start()
    player1 = game.players[0]

    deck_counter1 = DeckCounter(player1.get_all_cards())
    assert str(deck_counter1) == "7 Copper, 3 Estate"

    player1.gain(copper, game.supply)
    player1.gain(estate, game.supply)

    deck_counter2 = DeckCounter(player1.get_all_cards())
    assert str(deck_counter2) == "8 Copper, 4 Estate"