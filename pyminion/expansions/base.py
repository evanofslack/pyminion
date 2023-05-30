import logging
import math
from typing import TYPE_CHECKING, List, Tuple

from pyminion.core import AbstractDeck, CardType, Action, Card, Treasure, Victory
from pyminion.exceptions import EmptyPile
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Copper(Treasure):
    def __init__(
        self,
        name: str = "Copper",
        cost: int = 0,
        type: Tuple[CardType] = (CardType.Treasure,),
        money: int = 1,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: "Game"):
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Silver(Treasure):
    def __init__(
        self,
        name: str = "Silver",
        cost: int = 3,
        type: Tuple[CardType] = (CardType.Treasure,),
        money: int = 2,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: "Game"):

        # check if this is the first silver played and if there are any merchants in play
        if self not in player.playmat.cards:
            if num_merchants := len(
                [card for card in player.playmat.cards if card.name == "Merchant"]
            ):
                player.state.money += num_merchants

        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Gold(Treasure):
    def __init__(
        self,
        name: str = "Gold",
        cost: int = 6,
        type: Tuple[CardType] = (CardType.Treasure,),
        money: int = 3,
    ):
        super().__init__(name, cost, type, money)

    def play(self, player: Player, game: "Game"):
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money


class Estate(Victory):
    def __init__(
        self,
        name: str = "Estate",
        cost: int = 2,
        type: Tuple[CardType] = (CardType.Victory,),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = 1
        return vp


class Duchy(Victory):
    def __init__(
        self,
        name: str = "Duchy",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Victory,),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = 3
        return vp


class Province(Victory):
    def __init__(
        self,
        name: str = "Province",
        cost: int = 8,
        type: Tuple[CardType] = (CardType.Victory,),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = 6
        return vp


class Curse(Victory):
    def __init__(
        self,
        name: str = "Curse",
        cost: int = 0,
        type: Tuple[CardType] = (CardType.Curse,),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        vp = -1
        return vp


class Gardens(Victory):
    """
    Worth 1VP for every 10 cards you have (round down)

    """

    def __init__(
        self,
        name: str = "Gardens",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Victory,),
    ):
        super().__init__(name, cost, type)

    def score(self, player: Player) -> int:
        total_count = len(player.get_all_cards())
        vp = math.floor(total_count / 10)
        return vp


class Smithy(Action):
    """
    + 3 cards

    """

    def __init__(
        self,
        name: str = "Smithy",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action,),
        draw: int = 3,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(3)


class Village(Action):
    """
    + 1 card, + 2 actions

    """

    def __init__(
        self,
        name: str = "Village",
        cost: int = 3,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 2,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.draw()


class Laboratory(Action):
    """
    +2 cards, +1 action

    """

    def __init__(
        self,
        name: str = "Laboratory",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
        draw: int = 2,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw(2)


class Market(Action):
    """
    +1 card, +1 action, +1 money, +1 buy

    """

    def __init__(
        self,
        name: str = "Market",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
        draw: int = 1,
        money: int = 1,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()
        player.state.money += 1
        player.state.buys += 1


class Moneylender(Action):
    """
    You may trash a copper from your hand for + 3 money

    """

    def __init__(
        self,
        name: str = "Moneylender",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self,
        player: Player,
        game: "Game",
        generic_play: bool = True,
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        if copper not in player.hand.cards:
            return

        response = player.decider.binary_decision(
            prompt="Do you want to trash a copper from your hand for +3 money? y/n: ",
            card=self,
            player=player,
            game=game,
        )

        if response:
            player.trash(target_card=copper, trash=game.trash)
            player.state.money += 3


class Cellar(Action):
    """
    +1 Action

    Discard any number of cards, then draw that many

    """

    def __init__(
        self,
        name: str = "Cellar",
        cost: int = 2,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions)

    def play(
        self,
        player: Player,
        game: "Game",
        generic_play: bool = True,
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1

        if not player.hand.cards:
            return

        discard_cards = player.decider.discard_decision(
            prompt="Enter the cards you would like to discard separated by commas: ",
            card=self,
            valid_cards=player.hand.cards,
            player=player,
            game=game,
        )

        for card in discard_cards:
            player.discard(card)
        player.draw(len(discard_cards))


class Chapel(Action):
    """
    Trash up to 4 cards from your hand

    """

    def __init__(
        self,
        name: str = "Chapel",
        cost: int = 2,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        if not player.hand.cards:
            return

        trash_cards = player.decider.trash_decision(
            prompt="Enter up to 4 cards you would like to trash from your hand: ",
            card=self,
            valid_cards=player.hand.cards,
            player=player,
            game=game,
            min_num_trash=0,
            max_num_trash=4,
        )
        assert len(trash_cards) <= 4

        for card in trash_cards:
            player.trash(card, game.trash)


class Workshop(Action):
    """
    Gain a card costing up to 4 money

    """

    def __init__(
        self,
        name: str = "Workshop",
        cost: int = 3,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        gain_cards = player.decider.gain_decision(
            prompt="Gain a card costing up to 4 money: ",
            card=self,
            valid_cards=[
                card for card in game.supply.avaliable_cards() if card.get_cost(player, game) <= 4
            ],
            player=player,
            game=game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]
        assert gain_card.get_cost(player, game) <= 4

        player.gain(gain_card, game.supply)


class Festival(Action):
    """
    + 2 actions, + 1 buy, + 2 money

    """

    def __init__(
        self,
        name: str = "Festival",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 2,
        money: int = 2,
    ):
        super().__init__(name, cost, type, actions=actions, money=money)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2
        player.state.money += 2
        player.state.buys += 1


class Harbinger(Action):
    """
    +1 card, +1 action

    Look through your discard pile. You may put a card from it onto your deck

    """

    def __init__(
        self,
        name: str = "Harbinger",
        cost: int = 3,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.draw()

        if not player.discard_pile:
            return

        topdeck_cards = player.decider.topdeck_decision(
            prompt="You may select a card from your discard pile to put onto your deck: ",
            card=self,
            valid_cards=player.discard_pile.cards,
            player=player,
            game=game,
            min_num_topdeck=0,
            max_num_topdeck=1,
        )

        if len(topdeck_cards) == 0:
            return

        assert len(topdeck_cards) == 1
        topdeck_card = topdeck_cards[0]
        player.deck.add(player.discard_pile.remove(topdeck_card))


class Vassal(Action):
    """
    +2 money

    Discard the top card of your deck. If it's an action card you may play it.

    """

    def __init__(
        self,
        name: str = "Vassal",
        cost: int = 3,
        type: Tuple[CardType] = (CardType.Action,),
        money: int = 2,
    ):
        super().__init__(name, cost, type, money=money)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.money += 2
        player.draw(destination=player.discard_pile, silent=True)

        if not player.discard_pile:
            return

        discard_card = player.discard_pile.cards[-1]

        logger.info(f"{player} discards {discard_card}")

        if CardType.Action not in discard_card.type:
            return

        decision = player.decider.binary_decision(
            prompt=f"You discarded {discard_card.name}, would you like to play it? (y/n):  ",
            card=self,
            player=player,
            game=game,
        )

        if not decision:
            return

        played_card = player.discard_pile.cards.pop()
        player.playmat.add(played_card)
        player.exact_play(card=player.playmat.cards[-1], game=game, generic_play=False)
        return


class Artisan(Action):
    """
    Gain a card to your hand costing up to 5 money.

    Put a card from your hand onto your deck

    """

    def __init__(
        self,
        name: str = "Artisan",
        cost: int = 6,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        gain_cards = player.decider.gain_decision(
            prompt="Gain a card costing up to 5 money: ",
            card=self,
            valid_cards=[
                card for card in game.supply.avaliable_cards() if card.get_cost(player, game) <= 5
            ],
            player=player,
            game=game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]
        assert gain_card.get_cost(player, game) <= 5

        player.gain(card=gain_card, supply=game.supply, destination=player.hand)

        topdeck_cards = player.decider.topdeck_decision(
            prompt="Put a card from your hand onto your deck: ",
            card=self,
            valid_cards=player.hand.cards,
            player=player,
            game=game,
            min_num_topdeck=1,
            max_num_topdeck=1,
        )
        assert len(topdeck_cards) == 1
        topdeck_card = topdeck_cards[0]

        for card in player.hand.cards:
            if card == topdeck_card:
                player.deck.add(player.hand.remove(card))
                return


class Poacher(Action):
    """
    +1 card, +1 action, + 1 money

    Discard a card per empty Supply pile

    """

    def __init__(
        self,
        name: str = "Poacher",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
        draw: int = 1,
        money: int = 1,
    ):
        super().__init__(name, cost, type, actions, draw, money)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1
        player.state.money += 1

        empty_piles = game.supply.num_empty_piles()

        if empty_piles == 0:
            return

        discard_num = min(empty_piles, len(player.hand))

        discard_cards = player.decider.discard_decision(
            prompt=f"Discard {discard_num} card(s) from your hand: ",
            card=self,
            valid_cards=player.hand.cards,
            player=player,
            game=game,
            min_num_discard=discard_num,
            max_num_discard=discard_num,
        )
        assert len(discard_cards) == discard_num

        for discard_card in discard_cards:
            player.discard(discard_card)


class CouncilRoom(Action):
    """
    +4 cards, +1 buy

    Each other player draws a card

    """

    def __init__(
        self,
        name: str = "Council Room",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
        draw: int = 4,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(4)
        player.state.buys += 1

        for p in game.players:
            if p is not player:
                p.draw()


class Witch(Action):
    """
    +2 cards

    Each other player gains a curse

    """

    def __init__(
        self,
        name: str = "Witch",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action, CardType.Attack),
        draw: int = 2,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(2)

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(player=player, attack_card=self, game=game):

                    # attempt to gain a curse. if curse pile is empty, proceed
                    try:
                        opponent.gain(
                            card=curse,
                            supply=game.supply,
                        )
                    except EmptyPile:
                        pass


class Moat(Action):
    """
    +2 cards

    When another player plays an attack card, you may first
    reveal this from your hand, to be unaffected by it

    """

    def __init__(
        self,
        name: str = "Moat",
        cost: int = 2,
        type: Tuple[CardType] = (CardType.Action, CardType.Reaction),
        draw: int = 2,
    ):
        super().__init__(name, cost, type, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(2)


class Merchant(Action):
    """
    +1 card, +1 action

    The first time you play a Silver this turn, +1 money

    """

    def __init__(
        self,
        name: str = "Merchant",
        cost: int = 3,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw(1)
        player.state.actions += 1


class Bandit(Action):
    """
    Gain a Gold. Each other player reveals the top 2 cards of their deck,
    trashes a revealed treasure other than Copper, and discards the rest

    """

    def __init__(
        self,
        name: str = "Bandit",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action, CardType.Attack),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        # attempt to gain a gold. if gold pile is empty, proceed
        try:
            player.gain(card=gold, supply=game.supply)
        except EmptyPile:
            pass

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(player=player, attack_card=self, game=game):

                    revealed_cards = AbstractDeck()
                    opponent.draw(num_cards=2, destination=revealed_cards, silent=True)

                    logger.info(f"{opponent} reveals {revealed_cards}")

                    trash_card = None
                    for card in revealed_cards.cards:
                        if card.name == "Silver":
                            trash_card = card
                        elif card.name == "Gold" and not trash_card:
                            trash_card = card
                        elif (
                            CardType.Treasure in card.type
                            and card.name != "Copper"
                            and not trash_card
                        ):
                            trash_card = card

                    if trash_card:
                        game.trash.add(revealed_cards.remove(trash_card))

                    revealed_cards.move_to(opponent.discard_pile)
                    del revealed_cards


class Bureaucrat(Action):
    """
    Gain a Silver onto your deck. Each other player reveals a victory card from
    their hand and puts it onto their deck (or reveals a hand with no victory cards)

    """

    def __init__(
        self,
        name: str = "Bureaucrat",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action, CardType.Attack),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        # attempt to gain a silver. if silver pile is empty, proceed
        try:
            player.gain(card=silver, supply=game.supply, destination=player.deck)
        except EmptyPile:
            pass

        for opponent in game.players:
            if opponent is not player and opponent.is_attacked(
                player=player, attack_card=self, game=game
            ):

                victory_cards = []
                for card in opponent.hand.cards:
                    if CardType.Victory in card.type:
                        victory_cards.append(card)

                if not victory_cards:
                    logger.info(f"{opponent} reveals hand: {opponent.hand}")
                    continue

                topdeck_cards = opponent.decider.topdeck_decision(
                    prompt="You must topdeck a Victory card from your hand: ",
                    card=self,
                    valid_cards=victory_cards,
                    player=opponent,
                    game=game,
                    min_num_topdeck=1,
                    max_num_topdeck=1,
                )
                assert len(topdeck_cards) == 1
                topdeck_card = topdeck_cards[0]

                opponent.deck.add(opponent.hand.remove(topdeck_card))
                logger.info(f"{opponent} topdecks {topdeck_card}")


class ThroneRoom(Action):
    """
    You may play an Action card from your hand twice

    """

    def __init__(
        self,
        name: str = "Throne Room",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        action_cards = [card for card in player.hand.cards if CardType.Action in card.type]

        if not action_cards:
            return

        dp_card = player.decider.multi_play_decision(
            prompt="You may play an action card from your hand twice: ",
            card=self,
            valid_cards=action_cards,
            player=player,
            game=game,
            required=True,
        )
        assert dp_card is not None

        for card in player.hand.cards:
            if card.name == dp_card.name:
                player.playmat.add(player.hand.remove(card))
                state = None
                for i in range(2):
                    state = player.multi_play(card=card, game=game, state=state, generic_play=False)
                return


class Remodel(Action):
    """
    Trash a card from your hand. Gain a card costing up to $2 more than it

    """

    def __init__(
        self,
        name: str = "Remodel",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        trash_cards = player.decider.trash_decision(
            prompt="Trash a card form your hand: ",
            card=self,
            valid_cards=player.hand.cards,
            player=player,
            game=game,
            min_num_trash=1,
            max_num_trash=1,
        )
        assert len(trash_cards) == 1
        trash_card = trash_cards[0]

        max_cost = trash_card.get_cost(player, game) + 2
        gain_cards = player.decider.gain_decision(
            prompt=f"Gain a card costing up to {max_cost} money: ",
            card=self,
            valid_cards=[
                card
                for card in game.supply.avaliable_cards()
                if card.get_cost(player, game) <= max_cost
            ],
            player=player,
            game=game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]
        assert gain_card.get_cost(player, game) <= max_cost

        player.trash(trash_card, trash=game.trash)
        player.gain(gain_card, game.supply)


class Mine(Action):
    """
    You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to $3 more than it

    """

    def __init__(
        self,
        name: str = "Mine",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        treasures = [card for card in player.hand.cards if CardType.Treasure in card.type]

        if not treasures:
            return

        trash_cards = player.decider.trash_decision(
            prompt="You may trash a Treasure from your hand: ",
            card=self,
            valid_cards=treasures,
            player=player,
            game=game,
            min_num_trash=0,
            max_num_trash=1,
        )

        if len(trash_cards) == 0:
            return

        assert len(trash_cards) == 1
        trash_card = trash_cards[0]

        max_cost = trash_card.get_cost(player, game) + 3
        gain_cards = player.decider.gain_decision(
            prompt=f"Gain a Treasure card costing up to {max_cost} money to your hand: ",
            card=self,
            valid_cards=[
                card
                for card in game.supply.avaliable_cards()
                if CardType.Treasure in card.type and card.get_cost(player, game) <= trash_card.get_cost(player, game) + 3
            ],
            player=player,
            game=game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]
        assert CardType.Treasure in gain_card.type
        assert gain_card.get_cost(player, game) <= max_cost

        player.trash(trash_card, trash=game.trash)
        player.gain(gain_card, game.supply, destination=player.hand)


class Militia(Action):
    """
    +2 Money

    Each other player discards down to 3 cards in hand

    """

    def __init__(
        self,
        name: str = "Militia",
        cost: int = 4,
        type: Tuple[CardType] = (CardType.Action, CardType.Attack),
        money: int = 2,
    ):
        super().__init__(name, cost, type, money=money)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.money += 2

        for opponent in game.players:
            if opponent is not player and opponent.is_attacked(
                player=player, attack_card=self, game=game
            ):

                num_discard = len(opponent.hand) - 3
                if num_discard <= 0:
                    continue

                discard_cards = opponent.decider.discard_decision(
                    prompt=f"You must discard {num_discard} card(s) from your hand: ",
                    card=self,
                    valid_cards=opponent.hand.cards,
                    player=opponent,
                    game=game,
                    min_num_discard=num_discard,
                    max_num_discard=num_discard,
                )
                assert len(discard_cards) == num_discard

                for card in discard_cards:
                    opponent.discard(target_card=card)


class Sentry(Action):
    """
    +1 card, +1 action

    Look at the top 2 cards of your deck. Trash and/or discard any number of them. Put the rest back on top in any order

    """

    def __init__(
        self,
        name: str = "Sentry",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
        actions: int = 1,
        draw: int = 1,
    ):
        super().__init__(name, cost, type, actions=actions, draw=draw)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1

        revealed = AbstractDeck()
        player.draw(num_cards=2, destination=revealed, silent=True)
        logger.info(f"{player} looks at {revealed}")

        trash_cards = player.decider.trash_decision(
            prompt="Enter the cards you would like to trash: ",
            card=self,
            valid_cards=revealed.cards,
            player=player,
            game=game,
            min_num_trash=0,
            max_num_trash=2,
        )

        for card in trash_cards:
            revealed.remove(card)

        discard_cards: List[Card] = []
        if len(revealed.cards) > 0:
            discard_cards = player.decider.discard_decision(
                prompt="Enter the cards you would like to discard: ",
                card=self,
                valid_cards=revealed.cards,
                player=player,
                game=game,
            )
            for card in discard_cards:
                revealed.remove(card)

        reorder = False
        if len(revealed.cards) == 2:
            logger.info(
                f"Current order: {revealed.cards[0]} (Top), {revealed.cards[1]} (Bottom)"
            )
            reorder = player.decider.binary_decision(
                prompt="Would you like to switch the order of the cards?",
                card=self,
                player=player,
                game=game,
            )

        for card in trash_cards:
            game.trash.add(card)
            logger.info(f"{player} trashes {card}")
        for card in discard_cards:
            player.discard_pile.add(card)
            logger.info(f"{player} discards {card}")
        if revealed.cards:
            if reorder:
                for card in revealed.cards:
                    player.deck.add(card)
            else:
                for card in reversed(revealed.cards):
                    player.deck.add(card)
            logger.info(f"{player} topdecks {len(revealed.cards)} cards")


class Library(Action):
    """
    Draw until you have 7 cards in hand, skipping any Action cards you choose to; set those aside, discarding them afterwards

    """

    def __init__(
        self,
        name: str = "Library",
        cost: int = 5,
        type: Tuple[CardType] = (CardType.Action,),
    ):
        super().__init__(name, cost, type)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        set_aside = AbstractDeck()
        while len(player.hand) < 7:

            if len(player.deck) == 0 and len(player.discard_pile) == 0:
                return

            player.draw(num_cards=1, destination=set_aside)
            drawn_card = set_aside.cards[-1]

            if CardType.Action in drawn_card.type:
                should_skip = player.decider.binary_decision(
                    prompt=f"You drew {drawn_card}, would you like to skip it? y/n: ",
                    card=self,
                    player=player,
                    game=game,
                    relevant_cards=[drawn_card],
                )
                if not should_skip:
                    player.hand.add(set_aside.remove(drawn_card))

            else:
                player.hand.add(set_aside.remove(drawn_card))

        if set_aside.cards:
            logger.info(f"{player} discards {set_aside}")
            set_aside.move_to(destination=player.discard_pile)


copper = Copper()
silver = Silver()
gold = Gold()
estate = Estate()
duchy = Duchy()
province = Province()
curse = Curse()

artisan = Artisan()
bandit = Bandit()
bureaucrat = Bureaucrat()
cellar = Cellar()
chapel = Chapel()
council_room = CouncilRoom()
festival = Festival()
gardens = Gardens()
harbinger = Harbinger()
laboratory = Laboratory()
library = Library()
market = Market()
merchant = Merchant()
militia = Militia()
mine = Mine()
moat = Moat()
moneylender = Moneylender()
poacher = Poacher()
remodel = Remodel()
sentry = Sentry()
smithy = Smithy()
throne_room = ThroneRoom()
vassal = Vassal()
village = Village()
witch = Witch()
workshop = Workshop()


base_set: List[Card] = [
    artisan,
    bandit,
    bureaucrat,
    cellar,
    chapel,
    council_room,
    festival,
    gardens,
    harbinger,
    laboratory,
    library,
    market,
    merchant,
    militia,
    mine,
    moat,
    moneylender,
    poacher,
    remodel,
    sentry,
    smithy,
    throne_room,
    vassal,
    village,
    witch,
    workshop,
]
