from enum import IntEnum, unique
import logging
from typing import TYPE_CHECKING, List, Optional

from pyminion.core import AbstractDeck, Action, Card, CardType, Treasure
from pyminion.duration import (
    ActionDuration,
    BasicNextTurnEffect,
    GetSetAsideCardEffect,
    RemovePersistentCardsEffect,
)
from pyminion.effects import (
    AttackEffect,
    EffectAction,
    FuncPlayerGameEffect,
    PlayerCardGameEffect,
)
from pyminion.exceptions import EmptyPile
from pyminion.expansions.base import copper, curse
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class Astrolabe(Treasure):
    """
    Now and at the start of your next turn:
    $1
    +1 Buy

    """

    def __init__(self):
        super().__init__("Astrolabe", 3, (CardType.Treasure, CardType.Duration), 1)

    def play(self, player: Player, game: "Game") -> None:
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money
        player.state.buys += 1

        effect = BasicNextTurnEffect(
            f"{self.name}: +$1, +1 Buy", player, self, money=1, buys=1
        )
        game.effect_registry.register_turn_start_effect(effect)

        player.add_playmat_persistent_card(self)

        effect = RemovePersistentCardsEffect(player, [self])
        game.effect_registry.register_turn_start_effect(effect)


class Bazaar(Action):
    """
    +1 Card
    +2 Actions
    +$1

    """

    def __init__(self):
        super().__init__(
            name="Bazaar", cost=5, type=(CardType.Action,), draw=1, actions=2, money=1
        )


class Blockade(ActionDuration):
    """
    Gain a card costing up to $4, setting it aside.
    At the start of your next turn, put it into your hand. While it's set aside,
    when another player gains a copy of it on their turn, they gain a Curse.

    """

    class CurseEffect(PlayerCardGameEffect):
        def __init__(self, player: Player, card: Card):
            super().__init__(f"{blockade.name}: Gain curse")
            self.player = player
            self.card = card

        def get_action(self) -> EffectAction:
            return EffectAction.Other

        def is_triggered(self, player: Player, card: Card, game: "Game") -> bool:
            return player is not self.player and card.name == self.card.name and game.supply.pile_length("Curse") > 0

        def handler(self, player: Player, card: Card, game: "Game") -> None:
            player.gain(curse, game)

    def __init__(self):
        super().__init__(
            name="Blockade",
            cost=4,
            type=(CardType.Action, CardType.Duration, CardType.Attack),
        )

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:

        Action.play(self, player, game, generic_play)

        valid_cards = [
            card
            for card in game.supply.available_cards()
            if card.get_cost(player, game) <= 4
        ]
        gain_cards = player.decider.gain_decision(
            prompt="Gain a card costing up to 4 money: ",
            card=self,
            valid_cards=valid_cards,
            player=player,
            game=game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]
        assert gain_card.get_cost(player, game) <= 4

        player.set_aside.add(gain_card)

        get_set_aside_effect = GetSetAsideCardEffect(self.name, player, gain_cards)
        game.effect_registry.register_turn_start_effect(get_set_aside_effect)

        curse_effect = Blockade.CurseEffect(player, gain_card)
        game.effect_registry.register_gain_effect(curse_effect)

        unregister_effect = FuncPlayerGameEffect(
            f"{self.name}: Unregister Curse Effect",
            EffectAction.First,
            lambda p, g: g.effect_registry.unregister_gain_effects(
                curse_effect.get_name(), 1
            ),
            lambda p, g: p is player,
        )
        game.effect_registry.register_turn_start_effect(unregister_effect)

        self.persist(player, game, multi_play_card, count)


class Caravan(ActionDuration):
    """
    +1 Card
    +1 Action

    At the start of your next turn, +1 Card.

    """

    def __init__(self):
        super().__init__(
            name="Caravan",
            cost=4,
            type=(CardType.Action, CardType.Duration),
            draw=1,
            actions=1,
            next_turn_draw=1,
        )


class Cutpurse(Action):
    """
    +$2

    Each other player discards a Copper (or reveals a hand with no Copper).

    """

    def __init__(self):
        super().__init__(
            name="Cutpurse", cost=4, type=(CardType.Action, CardType.Attack), money=2
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        super().play(player, game, generic_play)

        for opponent in game.players:
            if opponent is not player and opponent.is_attacked(player, self, game):
                if copper in opponent.hand.cards:
                    opponent.discard(game, copper)
                else:
                    opponent.reveal(opponent.hand, game)


class FishingVillage(ActionDuration):
    """
    +2 Actions
    +$1

    At the start of your next turn:
    +1 Action and +$1.

    """

    def __init__(self):
        super().__init__(
            name="Fishing Village",
            cost=3,
            type=(CardType.Action, CardType.Duration),
            actions=2,
            money=1,
            next_turn_actions=1,
            next_turn_money=1,
        )


class Haven(ActionDuration):
    """
    +1 Card
    +1 Action

    Set aside a card from your hand face down (under this). At the start of your next turn,
    put it into your hand.

    """

    def __init__(self):
        super().__init__(
            name="Haven",
            cost=2,
            type=(CardType.Action, CardType.Duration),
            draw=1,
            actions=1,
        )

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:

        Action.play(self, player, game, generic_play)

        if len(player.hand) == 0:
            return

        set_aside_cards = player.decider.set_aside_decision(
            "Set aside a card from your hand: ",
            self,
            player.hand.cards,
            player,
            game,
            min_num_set_aside=1,
            max_num_set_aside=1,
        )
        assert len(set_aside_cards) == 1
        set_aside_card = set_aside_cards[0]

        player.hand.remove(set_aside_card)
        player.set_aside.add(set_aside_card)

        effect = GetSetAsideCardEffect(self.name, player, set_aside_cards)
        game.effect_registry.register_turn_start_effect(effect)

        self.persist(player, game, multi_play_card, count)


class Lighthouse(ActionDuration):
    """
    +1 Action
    +$1

    At the start of your next turn: +$1. Until then, when another player plays
    an Attack card, it doesn't affect you.

    """

    class BlockAttackEffect(AttackEffect):
        def __init__(self, player: Player):
            super().__init__(f"{lighthouse.name}: Block attack", EffectAction.Other)
            self.player = player

        def is_triggered(
            self,
            attacking_player: Player,
            defending_player: Player,
            attack_card: Card,
            game: "Game",
        ) -> bool:
            return defending_player is self.player

        def handler(
            self,
            attacking_player: Player,
            defending_player: Player,
            attack_card: Card,
            game: "Game",
        ) -> bool:
            return False

    def __init__(self):
        super().__init__(
            name="Lighthouse",
            cost=2,
            type=(CardType.Action, CardType.Duration),
            actions=1,
            money=1,
            next_turn_money=1,
        )

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:

        super().duration_play(player, game, multi_play_card, count, generic_play)

        block_effect = Lighthouse.BlockAttackEffect(player)
        game.effect_registry.register_attack_effect(block_effect)
        unregister_effect = FuncPlayerGameEffect(
            f"Unregister {lighthouse.name} Block",
            EffectAction.First,
            lambda p, g: g.effect_registry.unregister_attack_effects(
                block_effect.get_name(), 1
            ),
            lambda p, g: p is player,
        )
        game.effect_registry.register_turn_start_effect(unregister_effect)


class Lookout(Action):
    """
    +1 Action

    Look at the top 3 cards of your deck. Trash one of them. Discard one of them.
    Put the other one back on top of your deck.

    """

    def __init__(self):
        super().__init__(name="Lookout", cost=3, type=(CardType.Action,), actions=1)

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        super().play(player, game, generic_play)

        top_cards = AbstractDeck()
        player.draw(3, top_cards, silent=True)

        if len(top_cards) == 0:
            return

        # trash

        if len(top_cards) == 1:
            trash_card = top_cards.cards[0]
        else:
            trash_cards = player.decider.trash_decision(
                "Trash a card: ",
                self,
                top_cards.cards,
                player,
                game,
                min_num_trash=1,
                max_num_trash=1,
            )
            assert len(trash_cards) == 1
            trash_card = trash_cards[0]

        player.trash(trash_card, game, top_cards)

        if len(top_cards) == 0:
            return

        # discard

        if len(top_cards) == 1:
            discard_card = top_cards.cards[0]
        else:
            discard_cards = player.decider.discard_decision(
                "Discard a card: ",
                self,
                top_cards.cards,
                player,
                game,
                min_num_discard=1,
                max_num_discard=1,
            )
            assert len(discard_cards) == 1
            discard_card = discard_cards[0]

        player.discard(game, discard_card, top_cards)

        if len(top_cards) == 0:
            return

        # topdeck

        topdeck_card = top_cards.cards[0]
        player.deck.add(top_cards.remove(topdeck_card))
        logger.info(f"{player} topdecks {topdeck_card}")


class Monkey(ActionDuration):
    """
    Until your next turn, when the player to your right gains a card, +1 Card.
    At the start of your next turn, +1 Card.

    """

    class Effect(PlayerCardGameEffect):
        def __init__(self, played_player: Player, right_player: Player):
            super().__init__(f"{monkey.name}: Draw card")
            self.played_player = played_player
            self.right_player = right_player

        def get_action(self) -> EffectAction:
            return EffectAction.Last

        def is_triggered(self, player: Player, card: Card, game: "Game") -> bool:
            return player is self.right_player

        def handler(self, player: Player, card: Card, game: "Game") -> None:
            self.played_player.draw()

    def __init__(self):
        super().__init__(
            name="Monkey",
            cost=3,
            type=(CardType.Action, CardType.Duration),
            next_turn_draw=1,
        )

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:

        super().duration_play(player, game, multi_play_card, count, generic_play)

        right_player = game.get_right_player(player)
        draw_effect = Monkey.Effect(player, right_player)
        game.effect_registry.register_gain_effect(draw_effect)

        unregister_effect = FuncPlayerGameEffect(
            f"{self.name}: Unregister Draw",
            EffectAction.First,
            lambda p, g: g.effect_registry.unregister_gain_effects(
                draw_effect.get_name(), 1
            ),
            lambda p, g: p is player,
        )
        game.effect_registry.register_turn_start_effect(unregister_effect)


class NativeVillage(Action):
    """
    +2 Actions

    Choose one: Put the top card of your deck face down on your Native Village mat (you may look at
    those cards at any time); or put all the cards from your mat into your hand.

    """

    @unique
    class Choice(IntEnum):
        AddToMat = 0
        GetFromMat = 1

    def __init__(self):
        super().__init__(
            name="Native Village", cost=2, type=(CardType.Action,), actions=2
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        super().play(player, game, generic_play)

        mat = player.get_mat(self.name)
        mat_len = len(mat)
        plural = "" if mat_len == 1 else "s"

        options = [
            "Put the top card of your deck onto your Native Village mat",
        ]

        if mat_len == 0:
            options.append("Put no cards from your Native Village mat into your hand")
        else:
            s = f"Put the following card{plural} from your Native Village mat into your hand: "
            s += ", ".join(c.name for c in mat)
            options.append(s)

        choices = player.decider.multiple_option_decision(self, options, player, game)
        assert len(choices) == 1
        choice = choices[0]

        if choice == NativeVillage.Choice.AddToMat:
            player.draw(1, mat, silent=True)
            if len(mat) > mat_len:
                logger.info(f"{player} adds a card to their Native Village mat")
        elif choice == NativeVillage.Choice.GetFromMat:
            mat.move_to(player.hand)
            logger.info(
                f"{player} puts {mat_len} card{plural} from their Native Village mat into their hand"
            )
        else:
            raise ValueError(f"Unknown native village choice '{choice}'")


class SeaChart(Action):
    """
    +1 Card
    +1 Action

    Reveal the top card of your deck. If you have a copy of it in play, put it into your hand.

    """

    def __init__(self):
        super().__init__(
            name="Sea Chart", cost=3, type=(CardType.Action,), draw=1, actions=1
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        super().play(player, game, generic_play)

        revealed = AbstractDeck()
        player.draw(num_cards=1, destination=revealed, silent=True)
        if len(revealed) == 0:
            return

        revealed_card = revealed.cards[0]
        player.reveal(revealed_card, game)
        if revealed_card in player.playmat.cards:
            player.hand.add(revealed_card)
        else:
            player.deck.add(revealed_card)


class SeaWitch(ActionDuration):
    """
    +2 Cards

    Each other player gains a Curse.

    At the start of your next turn, +2 Cards, then discard 2 cards.

    """

    def __init__(self):
        super().__init__(
            name="Sea Witch",
            cost=5,
            type=(CardType.Action, CardType.Duration, CardType.Attack),
            draw=2,
            next_turn_draw=2,
            next_turn_discard=2,
        )

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:

        super().duration_play(player, game, multi_play_card, count, generic_play)

        for opponent in game.players:
            if opponent is not player:
                if opponent.is_attacked(
                    attacking_player=player, attack_card=self, game=game
                ):

                    # attempt to gain a curse. if curse pile is empty, proceed
                    try:
                        opponent.gain(
                            card=curse,
                            game=game,
                        )
                    except EmptyPile:
                        pass


class Smugglers(Action):
    """
    Gain a copy of a card costing up to $6 that the player to your
    right gained on their last turn.

    """

    def __init__(self):
        super().__init__(name="Smugglers", cost=3, type=(CardType.Action,))

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        super().play(player, game, generic_play)

        right_player = game.get_right_player(player)
        valid_cards: List[Card] = [
            card
            for card in right_player.last_turn_gains
            if card.get_cost(player, game) <= 6
            and game.supply.pile_length(card.name) > 0
        ]

        if len(valid_cards) == 0:
            return

        gain_cards = player.decider.gain_decision(
            "Choose a card to gain: ",
            self,
            valid_cards,
            player,
            game,
            min_num_gain=1,
            max_num_gain=1,
        )
        assert len(gain_cards) == 1
        gain_card = gain_cards[0]

        player.gain(gain_card, game)


class TidePools(ActionDuration):
    """
    +3 Cards
    +1 Action

    At the start of your next turn, discard 2 cards.

    """

    def __init__(self):
        super().__init__(
            name="Tide Pools",
            cost=4,
            type=(CardType.Action, CardType.Duration),
            draw=3,
            actions=1,
            next_turn_discard=2,
        )


class Warehouse(Action):
    """
    +3 Cards
    +1 Action

    Discard 3 cards.

    """

    def __init__(self):
        super().__init__(
            name="Warehouse",
            cost=3,
            type=(CardType.Action,),
            draw=3,
            actions=1,
            discard=3,
        )


class Wharf(ActionDuration):
    """
    Now and at the start of your next turn:
    +2 Cards and +1 Buy.

    """

    def __init__(self):
        super().__init__(
            name="Wharf",
            cost=5,
            type=(CardType.Action, CardType.Duration),
            draw=2,
            buys=1,
            next_turn_draw=2,
            next_turn_buys=1,
        )


astrolabe = Astrolabe()
bazaar = Bazaar()
blockade = Blockade()
caravan = Caravan()
cutpurse = Cutpurse()
fishing_village = FishingVillage()
haven = Haven()
lighthouse = Lighthouse()
lookout = Lookout()
monkey = Monkey()
native_village = NativeVillage()
sea_chart = SeaChart()
sea_witch = SeaWitch()
smugglers = Smugglers()
tide_pools = TidePools()
warehouse = Warehouse()
wharf = Wharf()


seaside_set: List[Card] = [
    astrolabe,
    bazaar,
    blockade,
    caravan,
    cutpurse,
    fishing_village,
    haven,
    lighthouse,
    lookout,
    monkey,
    native_village,
    sea_chart,
    sea_witch,
    smugglers,
    tide_pools,
    warehouse,
    wharf,
]
