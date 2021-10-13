import pytest

from app.models.cards import Deck, DiscardPile, Player, Hand, Playmat
from app.base_set.base_cards import copper, silver, gold, estate, duchy, province

NUM_COPPER = 7
NUM_ESTATE = 3


@pytest.fixture
def deck():
    start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]
    deck = Deck(cards=start_cards)
    return deck


@pytest.fixture
def player(deck):
    discard = DiscardPile()
    hand = Hand()
    playmat = Playmat()
    player = Player(deck=deck, discard=discard, hand=hand, playmat=playmat)
    return player


def test_create_player(deck):
    discard = DiscardPile()
    hand = Hand()
    playmat = Playmat()

    player = Player(deck=deck, discard=discard, hand=hand, playmat=playmat)
    assert len(player.deck) == 10
    assert len(player.discard) == 0
    assert len(player.hand) == 0
    assert len(player.playmat) == 0


def test_draw_deck_to_hand(player: Player):
    drawn_card = player.deck.draw()
    player.hand.add(drawn_card)
    assert len(player.hand) == 1
    assert len(player.deck) == 9


def test_draw_multiple_to_hand(player: Player):
    for i in range(5):
        player.hand.add(player.deck.draw())
    assert len(player.hand) == 5
    assert len(player.deck) == 5
