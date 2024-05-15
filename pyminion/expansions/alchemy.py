import logging
from typing import TYPE_CHECKING

from pyminion.core import (
    AbstractDeck,
    Action,
    Card,
    CardType,
    Cost,
    Treasure,
    Victory,
)
from pyminion.expansions.base import duchy, gold
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Potion(Treasure):
    def __init__(self):
        super().__init__("Potion", 4, (CardType.Treasure,), 0)

    def get_pile_starting_count(self, game: "Game") -> int:
        return 16

    def play(self, player: Player, game: "Game") -> None:
        super().play(player, game)

        player.state.potions += 1


class Apothecary(Action):
    """
    +1 Card
    +1 Action

    Reveal the top 4 cards of your deck. Put the Coppers and Potions into your hand.
    Put the rest back in any order.

    """

    def __init__(self):
        super().__init__(
            name="Apothecary",
            cost=Cost(money=2, potions=1),
            type=(CardType.Action,),
            draw=1,
            actions=1,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        revealed = AbstractDeck()
        player.draw(4, revealed)
        player.reveal(revealed, game)

        copper_potion_cards: list[Card] = []
        for card in revealed:
            if card.name in {"Copper", "Potion"}:
                copper_potion_cards.append(card)

        for card in copper_potion_cards:
            revealed.remove(card)
            player.hand.add(card)

        num_topdeck = len(revealed)

        if num_topdeck > 0:
            logger.info(f"Cards to topdeck: {revealed}")

        if num_topdeck <= 1:
            topdeck_cards = revealed.cards
        else:
            topdeck_cards = player.decider.topdeck_decision(
                prompt="Enter the cards in the order you would like to topdeck: ",
                card=self,
                valid_cards=revealed.cards,
                player=player,
                game=game,
                min_num_topdeck=num_topdeck,
                max_num_topdeck=num_topdeck,
            )

        for card in topdeck_cards:
            player.deck.add(card)


class Familiar(Action):
    """
    +1 Card
    +1 Action

    Each other player gains a Curse.

    """

    def __init__(self):
        super().__init__(
            name="Familiar",
            cost=Cost(money=3, potions=1),
            type=(CardType.Action, CardType.Attack),
            draw=1,
            actions=1,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        game.distribute_curses(player, self)


class Transmute(Action):
    """
    Trash a card from your hand.
    If it is an…
    Action card, gain a Duchy
    Treasure card, gain a Transmute
    Victory card, gain a Gold

    """

    def __init__(self):
        super().__init__(
            name="Transmute", cost=Cost(potions=1), type=(CardType.Action,)
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        if len(player.hand) == 0:
            return

        if len(player.hand) == 1:
            trash_card = player.hand.cards[0]
        else:
            trash_cards = player.decider.trash_decision(
                "Trash a card: ",
                self,
                player.hand.cards,
                player,
                game,
                min_num_trash=1,
                max_num_trash=1,
            )
            assert len(trash_cards) == 1
            trash_card = trash_cards[0]

        player.trash(trash_card, game)

        if CardType.Action in trash_card.type:
            player.try_gain(duchy, game)

        if CardType.Treasure in trash_card.type:
            player.try_gain(transmute, game)

        if CardType.Victory in trash_card.type:
            player.try_gain(gold, game)


class Vineyard(Victory):
    """
    Worth 1 VP per 3 Action cards you have (round down).

    """

    def __init__(self):
        super().__init__("Vineyard", Cost(potions=1), (CardType.Victory,))

    def score(self, player: Player) -> int:
        actions_count = sum(
            1 for card in player.get_all_cards() if CardType.Action in card.type
        )
        vp = actions_count // 3
        return vp


potion = Potion()

apothecary = Apothecary()
familiar = Familiar()
transmute = Transmute()
vineyard = Vineyard()


alchemy_set: list[Card] = [
    apothecary,
    familiar,
    transmute,
    vineyard,
]
