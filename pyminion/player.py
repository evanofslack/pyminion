import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable, Iterator

from pyminion.core import (AbstractDeck, Action, CardType, Card, Deck, DiscardPile, Hand,
                           Playmat, Supply, Trash, Treasure, get_action_cards, get_treasure_cards,
                           get_score_cards)
from pyminion.decider import Decider
from pyminion.exceptions import (CardNotFound, EmptyPile, InsufficientBuys,
                                 InsufficientMoney, InvalidCardPlay)

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


@dataclass
class State:
    """
    Hold state during a player's turn

    """

    actions: int = 1
    money: int = 0
    potions: int = 0
    buys: int = 1


class Player:
    """
    Basic representation of a player including the piles of cards they own
    and the basic actions they can take to manipulate the state of the game.

    """

    def __init__(
        self,
        decider: Decider,
        deck: Deck|None = None,
        discard_pile: DiscardPile|None = None,
        hand: Hand|None = None,
        playmat: Playmat|None = None,
        state: State|None = None,
        player_id: str = "",
    ):
        self.decider = decider
        self.deck = deck if deck else Deck()
        self.discard_pile = discard_pile if discard_pile else DiscardPile()
        self.hand = hand if hand else Hand()
        self.playmat = playmat if playmat else Playmat()
        self.set_aside = AbstractDeck()
        self.mats: dict[str, AbstractDeck] = {}
        self.state = state if state else State()
        self.player_id = player_id
        self.turns: int = 0
        self.shuffles: int = 0
        self.actions_played_this_turn: int = 0
        self.playmat_persist_counts: dict[str, int] = {}
        self.current_turn_gains: list[tuple[Game.Phase, Card]] = []
        self.last_turn_gains: list[tuple[Game.Phase, Card]] = []
        self.take_extra_turn: bool = False
        self.take_possession_turn: bool = False
        self.possessing_player: Player|None = None
        self.possession_trash = Trash()
        self.next_turn_draw: int = 5

    def __repr__(self):
        return f"{self.player_id}"

    def reset(self) -> None:
        """
        Reset the state of the player to a pre-game state.
        Required for resetting player deck and state between games when running simulations.

        """
        self.turns = 0
        self.shuffles = 0
        self.actions_played_this_turn = 0
        self.deck.cards = []
        self.discard_pile.cards = []
        self.hand.cards = []
        self.playmat.cards = []
        self.set_aside.cards = []
        self.mats = {}
        self.playmat_persist_counts = {}
        self.current_turn_gains = []
        self.last_turn_gains = []
        self.take_extra_turn = False
        self.take_possession_turn = False
        self.possessing_player = None
        self.next_turn_draw = 5

    def add_playmat_persistent_card(self, card: Card) -> None:
        name = card.name
        if name in self.playmat_persist_counts:
            self.playmat_persist_counts[name] += 1
        else:
            self.playmat_persist_counts[name] = 1

    def remove_playmat_persistent_card(self, card: Card) -> None:
        name = card.name
        assert self.playmat_persist_counts[name] > 0, f"self.playmat_persist_counts['{name}'] = {self.playmat_persist_counts[name]}"
        self.playmat_persist_counts[name] -= 1

    def get_mat(self, name: str) -> AbstractDeck:
        """
        Get a mat by name. If the mat does not exist, it is created.

        """
        mat = self.mats.get(name)
        if mat is None:
            mat = AbstractDeck()
            self.mats[name] = mat

        return mat

    def draw(
        self,
        num_cards: int = 1,
        destination: AbstractDeck|None = None,
        silent: bool = False,
    ) -> None:
        """
        Draw cards from deck and add them to the specified destination.
        Defaults to drawing one card and adding to the player's hand.

        By default, drawn cards and deck shuffles are logged.
        Call with silent = True to disable logging of drawn cards

        """
        if destination is None:
            destination = self.hand
        drawn_cards: AbstractDeck = AbstractDeck()
        for _ in range(num_cards):
            # Both deck and discard empty -> do nothing
            if len(self.discard_pile) == 0 and len(self.deck) == 0:
                pass
            else:
                # Deck is empty -> shuffle discard pile into deck
                if len(self.deck) == 0:
                    logger.info(f"{self} shuffles their deck")
                    self.discard_pile.move_to(self.deck)
                    self.deck.shuffle()
                    self.shuffles += 1

                draw_card = self.deck.draw()
                destination.add(draw_card)
                drawn_cards.add(draw_card)

        if not silent:
            logger.info(f"{self} draws {drawn_cards}")

    def discard(
            self,
            game: "Game",
            target_card: Card,
            source: AbstractDeck|None = None,
            silent: bool = False,
    ) -> None:
        """
        Move specified card from the player's hand to the player's discard pile.

        """
        if source is None:
            source = self.hand
        for card in source.cards:
            if card == target_card:
                self.discard_pile.add(source.remove(card))
                if not silent:
                    logger.info(f"{self} discards {card}")
                game.effect_registry.on_discard(self, card, game, source)
                return

    def play(self, target_card: Card, game: "Game", generic_play: bool = True) -> None:
        """
        Find target card in player's hand and play it.

        If generic_play is true, card is moved from player's hand to playmat
        and player action count decreased by 1. This is the default behavior
        but is overridden for cards like vassal and throne room.

        """
        if target_card not in self.hand.cards:
            raise CardNotFound(f"Invalid play, {target_card} not in hand")
        for card in self.hand.cards:
            if card.name == target_card.name:
                if CardType.Action in card.type:
                    assert isinstance(card, Action)
                    self.actions_played_this_turn += 1
                    card.play(player=self, game=game, generic_play=generic_play)
                    game.effect_registry.on_play(self, card, game)
                    return
                if CardType.Treasure in card.type:
                    assert isinstance(card, Treasure)
                    card.play(player=self, game=game)
                    game.effect_registry.on_play(self, card, game)
                    return
        raise InvalidCardPlay(f"Invalid play, {target_card} could not be played")

    def exact_play(self, card: Card, game: "Game", generic_play: bool = True) -> None:
        """
        Similar to previous play method, except exact card to play must be specified.
        This is method is necessary when playing cards not in the player's hand, such as vassal.

        """
        if CardType.Action in card.type:
            assert isinstance(card, Action)
            self.actions_played_this_turn += 1
            card.play(player=self, game=game, generic_play=generic_play)
            game.effect_registry.on_play(self, card, game)
        elif CardType.Treasure in card.type:
            assert isinstance(card, Treasure)
            card.play(player=self, game=game)
            game.effect_registry.on_play(self, card, game)
        else:
            raise InvalidCardPlay(f"Unable to play {card} with type {card.type}")

    def multi_play(self, card: Card, game: "Game", multi_play_card: Card, state: Any, generic_play: bool = True) -> Any:
        """
        Similar to previous exact_play method, except card's multi_play method is called.
        This method is necessary when playing "Throne Room variants".

        """
        if CardType.Action in card.type:
            assert isinstance(card, Action)
            self.actions_played_this_turn += 1
            state = card.multi_play(self, game, multi_play_card, state, generic_play)
            game.effect_registry.on_play(self, card, game)
        else:
            raise InvalidCardPlay(f"Unable to play {card} with type {card.type}")
        return state

    def buy(self, card: Card, game: "Game") -> None:
        """
        Buy a card from the supply and add to player's discard pile.
        Check that player has sufficient money and buys to gain the card.

        """
        assert isinstance(card, Card)
        cost = card.get_cost(self, game)
        if cost.money > self.state.money or cost.potions > self.state.potions:
            raise InsufficientMoney(
                f"{self.player_id}: Not enough money to buy {card.name}"
            )
        if self.state.buys < 1:
            raise InsufficientBuys(
                f"{self.player_id}: Not enough buys to buy {card.name}"
            )
        self.state.money -= cost.money
        self.state.potions -= cost.potions
        self.state.buys -= 1

        logger.info(f"{self} buys {card}")

        if self.possessing_player is None:
            try:
                game.supply.gain_card(card)
            except EmptyPile as e:
                raise e
            self.discard_pile.add(card)
            self.current_turn_gains.append((game.current_phase, card))
            game.effect_registry.on_buy(self, card, game, self.discard_pile)
        else:
            self.possessing_player.gain(card, game, destination=self.possessing_player.discard_pile)

    def gain(
        self,
        card: Card,
        game: "Game",
        destination: AbstractDeck|None = None,
        source: AbstractDeck|None = None,
    ) -> None:
        """
        Gain a card from source (supply by default) and adds it to destination.
        Defaults to adding the card to the player's discard pile.

        """
        if destination is None:
            destination = self.discard_pile
        if source is None:
            source = game.supply.get_pile(card.name)

        if self.possessing_player is None:
            gain_card = source.remove(card)
            destination.add(gain_card)
            self.current_turn_gains.append((game.current_phase, card))
            logger.info(f"{self} gains {gain_card}")
            game.effect_registry.on_gain(self, card, game, destination)
        else:
            self.possessing_player.gain(card, game, destination=self.possessing_player.discard_pile, source=source)

    def try_gain(
        self,
        card: Card,
        game: "Game",
        destination: AbstractDeck|None = None,
        source: AbstractDeck|None = None,
    ) -> None:
        """
        Gain a card from source (supply by default) and adds it to destination.
        Defaults to adding the card to the player's discard pile.
        If the source does not contain the card, nothing will happen.

        """
        try:
            self.gain(card, game, destination, source)
        except EmptyPile:
            # do nothing if the source was empty
            pass

    def trash(
        self, target_card: Card, game: "Game", source: AbstractDeck|None = None
    ) -> None:
        """
        Move a card from source to the trash.
        Defaults to moving the card from the player's hand.

        """
        if source is None:
            source = self.hand

        for card in source.cards:
            if card == target_card:
                source.remove(card)
                if self.possessing_player is None:
                    game.trash.add(card)
                else:
                    self.possession_trash.add(card)
                logger.info(f"{self} trashes {card}")
                game.effect_registry.on_trash(self, card, game)

                break

    def reveal(self, cards: Card|Iterable[Card], game: "Game", message: str|None = None) -> None:
        """
        Reveal cards.

        """
        if isinstance(cards, Card):
            cards = [cards]
        if message is None:
            message = f"{self} reveals "

        logger.info(message + ", ".join(card.name for card in cards))
        for card in cards:
            game.effect_registry.on_reveal(self, card, game)

    def topdeck(self, cards: Card|Iterable[Card], source: AbstractDeck) -> None:
        """
        Topdeck cards.

        """
        if isinstance(cards, Card):
            cards = [cards]

        logger.info(f"{self} topdecks " + ", ".join(card.name for card in cards))
        for card in cards:
            source.remove(card)
            self.deck.add(card)

    def start_turn(self, game: "Game", is_extra_turn: bool = False) -> None:
        """
        Increase turn counter and reset state

        """
        self.actions_played_this_turn = 0
        self.state.actions = 1
        self.state.money = 0
        self.state.potions = 0
        self.state.buys = 1

        if is_extra_turn:
            if self.possessing_player is None:
                logger.info(f"\nTurn {self.turns} (extra) - {self.player_id}")
            else:
                logger.info(f"\nTurn {self.turns} (possession) - {self.player_id} possessed by {self.possessing_player}")
        else:
            # extra turns do not count toward the total number of turns
            self.turns += 1
            logger.info(f"\nTurn {self.turns} - {self.player_id}")

        for mat_name in self.mats:
            mat = self.mats[mat_name]
            if len(mat) > 0:
                logger.info(f"{self.player_id}'s {mat_name} mat: {mat}")

        if len(self.playmat) > 0:
            logger.info(f"{self.player_id}'s cards in play: {self.playmat}")

        game.effect_registry.on_turn_start(self, game)

    def start_action_phase(self, game: "Game") -> None:
        game.current_phase = game.Phase.Action

        while self.state.actions > 0:
            logger.info(f"{self.player_id}'s hand: {self.hand}")

            viable_actions = [card for card in self.hand.cards if CardType.Action in card.type]
            if not viable_actions:
                return

            card = self.decider.action_phase_decision(viable_actions, self, game)
            if card is None:
                return

            self.play(card, game)

    def start_treasure_phase(self, game: "Game") -> None:
        game.current_phase = game.Phase.Buy

        viable_treasures = [card for card in self.hand.cards if CardType.Treasure in card.type]
        while len(viable_treasures) > 0:
            logger.info(f"Hand: {self.hand}")

            cards = self.decider.treasure_phase_decision(viable_treasures, self, game)
            if len(cards) == 0:
                break

            for card in cards:
                self.exact_play(card, game)
            cards_str = ", ".join([str(c) for c in cards])
            logger.info(f"{self.player_id} played {cards_str}")

            viable_treasures = [card for card in self.hand.cards if CardType.Treasure in card.type]

    def start_buy_phase(self, game: "Game") -> None:
        while self.state.buys > 0:
            logger.info(game.supply.get_pretty_string(self, game))
            logger.info(f"Money: {self.state.money}")
            if self.state.potions > 0:
                logger.info(f"Potions: {self.state.potions}")
            logger.info(f"Buys: {self.state.buys}")

            valid_cards = [
                c
                for c in game.supply.available_cards()
                if c.get_cost(self, game).money <= self.state.money and
                   c.get_cost(self, game).potions <= self.state.potions
            ]
            card = self.decider.buy_phase_decision(
                valid_cards=valid_cards,
                player=self,
                game=game,
            )

            if card is None:
                logger.info(f"{self} buys nothing")
                break

            self.buy(card, game)

        game.effect_registry.on_buy_phase_end(self, game)

    def start_cleanup_phase(self, game: "Game") -> None:
        """
        Move hand and playmat cards into discard pile and draw 5 new cards.

        """
        game.current_phase = game.Phase.CleanUp
        game.effect_registry.on_cleanup_phase_start(self, game)

        hand_copy = self.hand.cards[:]
        for card in hand_copy:
            self.discard(game, card, silent=True)

        persist_counts: dict[str, int] = {}
        playmat_copy = self.playmat.cards[:]
        for card in playmat_copy:
            persist_count = persist_counts.get(card.name, 0)
            target_persist_count = self.playmat_persist_counts.get(card.name, 0)
            if persist_count < target_persist_count:
                if card.name in persist_counts:
                    persist_counts[card.name] += 1
                else:
                    persist_counts[card.name] = 1
            else:
                self.discard(game, card, self.playmat, silent=True)

        self.draw(self.next_turn_draw)
        self.next_turn_draw = 5
        self.state.actions = 1
        self.state.money = 0
        self.state.potions = 0
        self.state.buys = 1

    def end_turn(self, game: "Game") -> None:
        game.effect_registry.on_turn_end(self, game)

        self.last_turn_gains = self.current_turn_gains
        self.current_turn_gains = []

    def take_turn(self, game: "Game", is_extra_turn: bool = False) -> None:
        self.start_turn(game, is_extra_turn)
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase(game)
        self.end_turn(game)

    def possess(self, game: "Game") -> None:
        opponent = game.get_left_player(self)

        # change opponent's decider
        original_decider = opponent.decider
        opponent.decider = self.decider
        opponent.possessing_player = self

        opponent.take_turn(game, is_extra_turn=True)

        if len(opponent.possession_trash) > 0:
            opponent.possession_trash.move_to(opponent.discard_pile)

        # reset opponent's state
        opponent.decider = original_decider
        opponent.possessing_player = None

        self.take_possession_turn = False

    def get_all_cards(self) -> Iterator[Card]:
        """
        Get all the cards the player has in their possession.

        """
        for card in self.deck:
            yield card

        for card in self.discard_pile:
            yield card

        for card in self.playmat:
            yield card

        for card in self.hand:
            yield card

        for card in self.set_aside:
            yield card

        for mat in self.mats.values():
            for card in mat:
                yield card

    def get_all_cards_count(self) -> int:
        """
        Get all the cards the player has in their possession.

        """
        return sum(1 for _ in self.get_all_cards())

    def get_card_count(self, card: Card) -> int:
        """
        Get count of a specific card in player's whole deck.

        """
        return sum(1 for c in self.get_all_cards() if c == card)

    def get_victory_points(self) -> int:
        """
        Return the number of victory points a player has.

        """
        total_vp: int = 0
        for card in get_score_cards(self.get_all_cards()):
            total_vp += card.score(self)
        return total_vp

    def get_treasure_money(self) -> int:
        """
        Return the amount of money a player has in their deck from treasure cards.

        """
        total_money: int = 0
        for card in get_treasure_cards(self.get_all_cards()):
            total_money += card.money
        return total_money

    def get_action_money(self) -> int:
        """
        Return the amount of money a player has in their deck from action cards.

        """
        total_money: int = 0
        for card in get_action_cards(self.get_all_cards()):
            total_money += card.money
        return total_money

    def get_deck_money(self) -> int:
        """
        Return total count of all money a player has in their deck.

        """
        treasure_money = self.get_treasure_money()
        action_money = self.get_action_money()
        return treasure_money + action_money

    def is_attacked(self, attacking_player: "Player", attack_card: Card, game: "Game") -> bool:
        attacked = game.effect_registry.on_attack(attacking_player, self, attack_card, game)
        return attacked
