from models.cards import Deck, Card, Treasure, Victory
from base_set.base_cards import copper, silver, gold, estate, duchy, province

NUM_COPPER = 7
NUM_ESTATE = 3

start_cards = [copper for x in range(NUM_COPPER)] + [
        estate for x in range(NUM_ESTATE)
    ]

deck = Deck(cards=start_cards)

for card in deck.cards:
    print (card)

deck.shuffle()

for card in deck.cards:
    print (card)
