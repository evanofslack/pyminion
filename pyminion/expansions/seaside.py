from enum import IntEnum, unique
import logging
from typing import TYPE_CHECKING, Any, List, Optional

from pyminion.core import AbstractDeck, Action, Card, CardType, Treasure
from pyminion.effects import (
    AttackEffect,
    EffectAction,
    FuncPlayerGameEffect,
    PlayerGameEffect,
)
from pyminion.expansions.base import copper
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class BasicNextTurnEffect(PlayerGameEffect):
    def __init__(
        self,
        name: str,
        player: Player,
        card: Card,
        draw: int = 0,
        actions: int = 0,
        money: int = 0,
        buys: int = 0,
        discard: int = 0,
    ):
        super().__init__(name)
        self.player = player
        self.card = card
        self.draw = draw
        self.actions = actions
        self.money = money
        self.buys = buys
        self.discard = discard

    def get_action(self) -> EffectAction:
        if self.draw > 0 and self.discard > 0:
            return EffectAction.HandAddRemoveCards
        elif self.draw > 0:
            return EffectAction.HandAddCards
        elif self.discard > 0:
            return EffectAction.HandRemoveCards
        else:
            return EffectAction.Other

    def is_triggered(self, player: Player, game: "Game") -> bool:
        return player is self.player

    def handler(self, player: Player, game: "Game") -> None:
        if self.draw > 0:
            player.draw(self.draw)

        player.state.actions += self.actions
        player.state.money += self.money
        player.state.buys += self.buys

        if self.discard > 0 and len(player.hand) > 0:
            if len(player.hand) <= self.discard:
                discard_cards = player.hand.cards[:]
            else:
                discard_cards = player.decider.discard_decision(
                    prompt=f"Discard {self.discard} card(s) from your hand: ",
                    card=self.card,
                    valid_cards=player.hand.cards,
                    player=player,
                    game=game,
                    min_num_discard=self.discard,
                    max_num_discard=self.discard,
                )
                assert len(discard_cards) == self.discard

            for discard_card in discard_cards:
                player.discard(game, discard_card)

        game.effect_registry.unregister_turn_start_effects(self.get_name(), 1)


class RemovePersistentCardsEffect(PlayerGameEffect):
    def __init__(self, player: Player, cards: List[Card]):
        super().__init__("Remove Persistent Cards")
        self.player = player
        self.cards = cards

    def get_action(self) -> EffectAction:
        return EffectAction.Other

    def is_triggered(self, player: Player, game: "Game") -> bool:
        return player is self.player

    def handler(self, player: Player, game: "Game") -> None:
        for card in self.cards:
            player.remove_playmat_persistent_card(card)

        game.effect_registry.unregister_turn_start_effects(self.get_name(), 1)


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

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 2
        player.state.money += 1


class Caravan(Action):
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
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        self.duration_play(player, game, None, 1, generic_play)

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

        self.duration_play(player, game, multi_play_card, count, generic_play)

        return count

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:
        if count == 1:
            persistent_cards: List[Card] = [self]
            if multi_play_card is not None:
                persistent_cards.append(multi_play_card)

            for card in persistent_cards:
                player.add_playmat_persistent_card(card)

            effect = RemovePersistentCardsEffect(player, persistent_cards)
            game.effect_registry.register_turn_start_effect(effect)

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1

        effect = BasicNextTurnEffect(f"{self.name}: +1 Card", player, self, draw=1)
        game.effect_registry.register_turn_start_effect(effect)


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

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.money += 2

        for opponent in game.players:
            if opponent is not player and opponent.is_attacked(player, self, game):
                if copper in opponent.hand.cards:
                    opponent.discard(game, copper)
                else:
                    opponent.reveal(opponent.hand.cards, game)


class Lighthouse(Action):
    """
    +1 Action
    +$1

    At the start of your next turn: +$1. Until then, when another player plays
    an Attack card, it doesn't affect you.

    """

    class BlockAttackEffect(AttackEffect):
        def __init__(self, player: Player):
            super().__init__(f"{lighthouse.name}: Block Attack", EffectAction.Other)
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
        )

    def play(self, player: Player, game: "Game", generic_play: bool = True) -> None:
        self.duration_play(player, game, None, 1, generic_play)

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

        self.duration_play(player, game, multi_play_card, count, generic_play)

        return count

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:
        if count == 1:
            persistent_cards: List[Card] = [self]
            if multi_play_card is not None:
                persistent_cards.append(multi_play_card)

            for card in persistent_cards:
                player.add_playmat_persistent_card(card)

            effect = RemovePersistentCardsEffect(player, persistent_cards)
            game.effect_registry.register_turn_start_effect(effect)

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.state.actions += 1
        player.state.money += 1

        effect = BasicNextTurnEffect(f"{self.name}: +$1", player, self, money=1)
        game.effect_registry.register_turn_start_effect(effect)

        block_effect = Lighthouse.BlockAttackEffect(player)
        game.effect_registry.register_attack_effect(block_effect)
        unregister_effect = FuncPlayerGameEffect(
            f"Unregister {lighthouse.name} Block",
            EffectAction.Other,
            lambda p, g: g.effect_registry.unregister_attack_effects(
                block_effect.get_name(), 1
            ),
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

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.state.actions += 2

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
            s += ", ".join(c.name for c in mat.cards)
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
            logger.info(f"{player} puts {mat_len} card{plural} from their Native Village mat into their hand")
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

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1

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


astrolabe = Astrolabe()
bazaar = Bazaar()
caravan = Caravan()
cutpurse = Cutpurse()
lighthouse = Lighthouse()
native_village = NativeVillage()
sea_chart = SeaChart()


seaside_set: List[Card] = [
    astrolabe,
    bazaar,
    caravan,
    cutpurse,
    lighthouse,
    native_village,
    sea_chart,
]
