from base_cards import copper
from models.cards import Pile


copper_pile = Pile(cards=[copper for x in range(40)])


for card in copper_pile.cards:
    print(card.name)
