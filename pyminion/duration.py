from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from pyminion.core import Action, Card, CardType
from pyminion.effects import EffectAction, PlayerGameEffect
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


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
        return EffectAction.First

    def is_triggered(self, player: Player, game: "Game") -> bool:
        return player is self.player

    def handler(self, player: Player, game: "Game") -> None:
        for card in self.cards:
            player.remove_playmat_persistent_card(card)

        game.effect_registry.unregister_turn_start_effects(self.get_name(), 1)


class ActionDuration(Action):
    """
    Base class for Action-Duration cards.

    """

    def __init__(
        self,
        name: str,
        cost: int,
        type: Tuple[CardType, ...],
        actions: int = 0,
        draw: int = 0,
        money: int = 0,
        buys: int = 0,
        discard: int = 0,
        next_turn_actions: int = 0,
        next_turn_draw: int = 0,
        next_turn_money: int = 0,
        next_turn_buys: int = 0,
        next_turn_discard: int = 0,
    ):
        super().__init__(name, cost, type, actions, draw, money, buys, discard)
        self.next_turn_actions = next_turn_actions
        self.next_turn_draw = next_turn_draw
        self.next_turn_money = next_turn_money
        self.next_turn_buys = next_turn_buys
        self.next_turn_discard = next_turn_discard

    def _get_effect_name(self) -> str:
        effects: List[str] = []
        if self.next_turn_draw > 0:
            p = "s" if self.next_turn_draw > 1 else ""
            effects.append(f"+{self.next_turn_draw} Card{p}")
        if self.next_turn_actions > 0:
            p = "s" if self.next_turn_actions > 1 else ""
            effects.append(f"+{self.next_turn_actions} Action{p}")
        if self.next_turn_buys > 0:
            p = "s" if self.next_turn_buys > 1 else ""
            effects.append(f"+{self.next_turn_buys} Buys{p}")
        if self.next_turn_money > 0:
            effects.append(f"+${self.next_turn_money}")
        if self.next_turn_discard > 0:
            p = "s" if self.next_turn_discard > 1 else ""
            effects.append(f"discard {self.next_turn_discard} card{p}")

        name = f"{self.name}: " + ",".join(effects)
        return name

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

    def persist(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
    ) -> None:
        if count == 1:
            persistent_cards: List[Card] = [self]
            if multi_play_card is not None:
                persistent_cards.append(multi_play_card)

            for card in persistent_cards:
                player.add_playmat_persistent_card(card)

            effect = RemovePersistentCardsEffect(player, persistent_cards)
            game.effect_registry.register_turn_start_effect(effect)

    def duration_play(
        self,
        player: Player,
        game: "Game",
        multi_play_card: Optional[Card],
        count: int,
        generic_play: bool = True,
    ) -> None:

        super().play(player, game, generic_play)

        self.persist(player, game, multi_play_card, count)

        if (
            self.next_turn_draw > 0
            or self.next_turn_actions > 0
            or self.next_turn_money > 0
            or self.next_turn_buys > 0
            or self.next_turn_discard > 0
        ):
            effect = BasicNextTurnEffect(
                self._get_effect_name(),
                player,
                self,
                self.next_turn_draw,
                self.next_turn_actions,
                self.next_turn_money,
                self.next_turn_buys,
                self.next_turn_discard,
            )
            game.effect_registry.register_turn_start_effect(effect)
