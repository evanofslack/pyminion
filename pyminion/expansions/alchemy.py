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
from pyminion.effects import (
    EffectAction,
    FuncPlayerGameEffect,
    PlayerGameEffect,
    PlayerCardGameDeckEffect,
)
from pyminion.expansions.base import duchy, gold
from pyminion.player import Player
from typing import Any

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


class Alchemist(Action):
    """
    +2 Cards
    +1 Action

    At the start of Clean-up this turn, if you have a Potion in play,
    you may put this onto your deck.

    """

    class TopdeckEffect(PlayerGameEffect):
        def __init__(self, card: Card):
            super().__init__("Alchemist: Topdeck")
            self.card = card

        def get_action(self) -> EffectAction:
            return EffectAction.Other

        def is_triggered(self, player: Player, game: "Game") -> bool:
            has_potion = any(card.name == "Potion" for card in player.playmat)
            return has_potion

        def handler(self, player: Player, game: "Game") -> None:
            topdeck = player.decider.binary_decision(
                "Would you like to topdeck Alchemist? (y/n): ",
                self.card,
                player,
                game,
            )

            if topdeck:
                player.topdeck(self.card, player.playmat)

    class UnregisterEffect(PlayerGameEffect):
        def __init__(self, unregister_id: int):
            super().__init__("Alchemist: Unregister topdeck")
            self.unregister_id = unregister_id

        def get_action(self) -> EffectAction:
            return EffectAction.Last

        def is_triggered(self, player: Player, game: "Game") -> bool:
            return True

        def handler(self, player: Player, game: "Game") -> None:
            game.effect_registry.unregister_cleanup_phase_start_effect(
                self.unregister_id
            )
            game.effect_registry.unregister_turn_end_effect(self.get_id())

    def __init__(self):
        super().__init__(
            name="Alchemist",
            cost=Cost(money=3, potions=1),
            type=(CardType.Action,),
            draw=2,
            actions=1,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        self._play(player, game, 1, generic_play)

    def multi_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Card,
        state: Any,
        generic_play: bool = True,
    ) -> Any:
        if state is None:
            count = 1
        else:
            count = int(state) + 1

        self._play(player, game, count, generic_play)

        return count

    def _play(
        self, player: Player, game: "Game", count: int, generic_play: bool = True
    ) -> None:
        super().play(player, game, generic_play)

        if count == 1:
            topdeck_effect = Alchemist.TopdeckEffect(self)
            game.effect_registry.register_cleanup_phase_start_effect(topdeck_effect)

            unregister_effect = Alchemist.UnregisterEffect(topdeck_effect.get_id())
            game.effect_registry.register_turn_end_effect(unregister_effect)


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
        player.draw(4, revealed, silent=True)
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
            topdeck_cards = revealed.cards[:]
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

        player.topdeck(topdeck_cards, revealed)


class Apprentice(Action):
    """
    +1 Action

    Trash a card from your hand.
    +1 Card per $1 it costs.
    +2 Cards if it has P in its cost.

    """

    def __init__(self):
        super().__init__(
            name="Apprentice",
            cost=5,
            type=(CardType.Action,),
            actions=1,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        if len(player.hand) == 0:
            return

        if len(player.hand) == 1:
            trash_card = player.hand.cards[0]
        else:
            trash_cards = player.decider.trash_decision(
                "Choose a card to trash",
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

        cost = trash_card.get_cost(player, game)

        num_draw = cost.money
        if cost.potions > 0:
            num_draw += 2

        player.draw(num_draw)


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


class Golem(Action):
    """
    Reveal cards from your deck until you reveal 2 Action cards other than Golems.
    Discard the other cards, then play the Action cards in either order.

    """

    def __init__(self):
        super().__init__(
            name="Golem",
            cost=Cost(money=4, potions=1),
            type=(CardType.Action,),
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        action_cards = AbstractDeck()
        other_cards = AbstractDeck()
        while len(action_cards) < 2 and len(player.deck) + len(player.discard_pile) > 0:
            temp = AbstractDeck()
            player.draw(1, temp, silent=True)
            revealed_card = temp.cards[0]
            player.reveal(revealed_card, game)

            if CardType.Action in revealed_card.type and revealed_card.name != "Golem":
                temp.move_to(action_cards)
            else:
                temp.move_to(other_cards)

        while len(other_cards) > 0:
            player.discard(game, other_cards.cards[0], other_cards)

        if len(action_cards) == 0:
            return

        ordered_cards: list[Card]
        if len(action_cards) == 1:
            ordered_cards = [action_cards.cards[0]]
        else:
            options = [
                f"Play {action_cards.cards[0]} first",
                f"Play {action_cards.cards[1]} first",
            ]
            choices = player.decider.multiple_option_decision(
                self,
                options,
                player,
                game,
            )
            assert len(choices) == 1
            choice = choices[0]

            ordered_cards = action_cards.cards[:]
            if choice == 1:
                ordered_cards.reverse()

        for card in ordered_cards:
            player.playmat.add(card)
            player.exact_play(card, game, generic_play=False)


class Herbalist(Action):
    """
    +1 Buy
    +$1

    Once this turn, when you discard a Treasure from play, you may put it onto your deck.

    """

    class TopdeckTreasureEffect(PlayerCardGameDeckEffect):
        def __init__(self, herbalist: "Herbalist", players: list[Player]):
            super().__init__("Herbalist: Topdeck Treasure")
            self.herbalist = herbalist
            self.player_herbalist_counts: dict[str, int] = {}
            for player in players:
                self.player_herbalist_counts[player.player_id] = 0

        def get_action(self) -> EffectAction:
            return EffectAction.Other

        def is_triggered(
            self, player: Player, card: Card, game: "Game", deck: AbstractDeck
        ) -> bool:
            herbalist_counts = self.player_herbalist_counts.get(player.player_id, 0)
            return (
                herbalist_counts > 0
                and deck is player.playmat
                and CardType.Treasure in card.type
            )

        def handler(
            self, player: Player, card: Card, game: "Game", deck: AbstractDeck
        ) -> None:
            topdeck = player.decider.binary_decision(
                f"Do you want to topdeck {card}? y/n: ",
                self.herbalist,
                player,
                game,
                relevant_cards=[card],
            )

            if topdeck:
                player.topdeck(card, player.discard_pile)
                self.player_herbalist_counts[player.player_id] -= 1

    def __init__(self):
        super().__init__(
            name="Herbalist",
            cost=2,
            type=(CardType.Action,),
            buys=1,
            money=1,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        effects = [
            e
            for e in game.effect_registry.discard_effects
            if e.get_name() == "Herbalist: Topdeck Treasure"
        ]
        assert len(effects) == 1
        topdeck_effect = effects[0]
        assert isinstance(topdeck_effect, Herbalist.TopdeckTreasureEffect)
        topdeck_effect.player_herbalist_counts[player.player_id] += 1

    def set_up(self, game: "Game") -> None:
        # register play treasure effect
        topdeck_effect = Herbalist.TopdeckTreasureEffect(self, game.players)
        game.effect_registry.register_discard_effect(topdeck_effect)

        def reset_count(p: Player, g: "Game"):
            topdeck_effect.player_herbalist_counts[p.player_id] = 0

        # reset herbalist counts at the end of each turn
        reset_effect = FuncPlayerGameEffect(
            f"{self.name}: Reset count",
            EffectAction.Last,
            reset_count,
        )
        game.effect_registry.register_turn_end_effect(reset_effect)


class PhilosophersStone(Treasure):
    """
    Count your deck and discard pile.
    +$1 per 5 cards total between them (round down).

    """

    def __init__(self):
        super().__init__(
            "Philosopher's Stone", Cost(money=3, potions=1), (CardType.Treasure,), 0
        )

    def play(self, player: Player, game: "Game") -> None:
        super().play(player, game)

        count = len(player.deck) + len(player.discard_pile)
        money = count // 5
        player.state.money += money


class Possession(Action):
    """
    The player to your left takes an extra turn after this one (but not a 2nd
    extra turn in a row), in which you can see all cards they can and make all
    decisions for them. Any cards or debt they would gain on that turn, you gain
    instead; any cards of theirs that are trashed are set aside and put in their
    discard pile at end of turn.

    """

    def __init__(self):
        super().__init__(
            name="Possession",
            cost=Cost(money=6, potions=1),
            type=(CardType.Action,),
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        player.take_possession_turn = True


class ScryingPool(Action):
    """
    +1 Action

    Each player (including you) reveals the top card of their deck and either
    discards it or puts it back, your choice. Then reveal cards from your deck
    until revealing one that isn't an Action. Put all of those revealed cards
    into your hand.

    """

    def __init__(self):
        super().__init__(
            name="Scrying Pool",
            cost=Cost(money=2, potions=1),
            type=(CardType.Action, CardType.Attack),
            actions=1,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        # player checks their top card
        self._check_top_card(player, player, game)

        # player checks all opponents top cards
        for opponent in game.get_opponents(player):
            if opponent.is_attacked(player, self, game):
                self._check_top_card(player, opponent, game)

        # reveal cards until we find a non-Action card
        revealed = AbstractDeck()
        while len(player.deck) > 0 or len(player.discard_pile) > 0:
            player.draw(1, revealed, silent=True)
            card = revealed.cards[-1]
            player.reveal(card, game)
            if CardType.Action not in card.type:
                break

        revealed.move_to(player.hand)

    def _check_top_card(
        self, attacking_player: Player, defending_player: Player, game: "Game"
    ) -> None:
        revealed = AbstractDeck()
        defending_player.draw(1, revealed, silent=True)
        if len(revealed) == 0:
            return

        revealed_card = revealed.cards[0]
        defending_player.reveal(revealed_card, game)

        if attacking_player is defending_player:
            prompt = f"Discard your {revealed_card}? (y/n): "
        else:
            prompt = f"Discard {defending_player}'s {revealed_card}? (y/n): "

        discard = attacking_player.decider.binary_decision(
            prompt,
            self,
            attacking_player,
            game,
            relevant_cards=[revealed_card],
        )

        if discard:
            defending_player.discard(game, revealed_card, revealed)
        else:
            defending_player.deck.add(revealed_card)


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


class University(Action):
    """
    +2 Actions

    You may gain an Action card costing up to $5.

    """

    def __init__(self):
        super().__init__(
            name="University",
            cost=Cost(money=2, potions=1),
            type=(CardType.Action,),
            actions=2,
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        super().play(player, game, generic_play)

        valid_cards = [
            card
            for card in game.supply.available_cards()
            if CardType.Action in card.type and card.get_cost(player, game) <= 5
        ]
        if len(valid_cards) == 0:
            return

        gain = player.decider.binary_decision(
            prompt="Do you want to gain an Action card costing up to 5 money? (y/n): ",
            card=self,
            player=player,
            game=game,
        )
        if not gain:
            return

        gain_cards = player.decider.gain_decision(
            prompt="Gain a card costing up to 5 money: ",
            card=self,
            valid_cards=valid_cards,
            player=player,
            game=game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]
        assert gain_card.get_cost(player, game) <= 5

        player.gain(gain_card, game)


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

alchemist = Alchemist()
apothecary = Apothecary()
apprentice = Apprentice()
familiar = Familiar()
golem = Golem()
herbalist = Herbalist()
philosophers_stone = PhilosophersStone()
possession = Possession()
scrying_pool = ScryingPool()
transmute = Transmute()
university = University()
vineyard = Vineyard()


alchemy_set: list[Card] = [
    alchemist,
    apothecary,
    apprentice,
    familiar,
    golem,
    herbalist,
    philosophers_stone,
    possession,
    scrying_pool,
    transmute,
    university,
    vineyard,
]
