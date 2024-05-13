import logging
from typing import TYPE_CHECKING

from pyminion.core import (
    Action,
    Card,
    CardType,
    Cost,
    Treasure,
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


potion = Potion()

transmute = Transmute()


alchemy_set: list[Card] = [
    transmute,
]
