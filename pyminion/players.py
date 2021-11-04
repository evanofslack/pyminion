from pyminion.models.core import Player, Deck
from pyminion.game import Game
from pyminion.decisions import single_card_decision, validate_input
from pyminion.exceptions import InvalidSingleCardInput, InsufficientMoney
import sys
from io import StringIO

from contextlib import contextmanager


@contextmanager
def input_redirect(input: str):
    saved_input = sys.stdin
    sys.stdin = StringIO(input)
    yield
    sys.stdin = saved_input


class InputRedirect:
    """
    Context manager to mock the input() calls required to make decisions

    """

    def __init__(self, input: str):
        self.input = input

    def __enter__(self):
        self.saved_input = sys.stdin
        sys.stdin = StringIO(self.input)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdin = self.saved_input


class Human(Player):
    """
    Human player can make choices as to which cards
    to play and buy in real time through the terminal

    """

    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "human",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def start_turn(self):
        print(f"\nTurn {self.turns} ({self.player_id})")
        self.turns += 1
        self.state.actions = 1
        self.state.money = 0
        self.state.buys = 1

    def start_action_phase(self, game: Game):
        viable_actions = [card for card in self.hand.cards if card.type == "Action"]
        while viable_actions and self.state.actions:

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_action(game: Game) -> bool:
                print(self.hand)
                card = single_card_decision(
                    prompt="Choose an action card to play: ",
                    valid_cards=viable_actions,
                )
                if not card:
                    return False
                self.play(card, game)
                print(f"{self.player_id} played {card}")
                viable_actions.remove(card)
                return True

            if not choose_action(game):
                return

    def start_treasure_phase(self, game: Game):
        viable_treasures = [card for card in self.hand.cards if card.type == "Treasure"]
        while viable_treasures:

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_treasure(game: Game):
                print(self.hand)
                card = single_card_decision(
                    prompt="Choose an treasure card to play or 'all' to autoplay treasures: ",
                    valid_cards=viable_treasures,
                    valid_mixin="all",
                )
                if not card:
                    return False
                if card == "all":
                    i = 0
                    while i < len(viable_treasures):
                        self.exact_play(viable_treasures[i], game)
                        viable_treasures.remove(viable_treasures[i])
                    return True
                self.exact_play(card, game)
                print(f"{self.player_id} played {card}")
                viable_treasures.remove(card)
                return True

            if not choose_treasure(game):
                return

    def start_buy_phase(self, game: Game):
        while self.state.buys and self.state.money:
            print("Money: ", self.state.money)
            print("Buys: ", self.state.buys)

            @validate_input(exceptions=(InvalidSingleCardInput, InsufficientMoney))
            def choose_buy(game: Game) -> bool:
                card = single_card_decision(
                    prompt="Choose a card to buy: ",
                    valid_cards=game.supply.avaliable_cards(),
                )
                if not card:
                    return False
                self.buy(card, game.supply)
                print(f"{self.player_id} bought {card}")
                return True

            if not choose_buy(game):
                return

    def start_cleanup_phase(self):
        self.discard_pile.cards += self.hand.cards
        self.discard_pile.cards += self.playmat.cards
        self.hand.cards = []
        self.playmat.cards = []
        self.draw(5)

    def take_turn(self, game: Game) -> None:
        self.start_turn()
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()


class BigMoney(Human):
    """
    Only buys money and provinces

    """

    def __init__(
        self,
        deck: Deck = None,
        player_id: str = "big_money",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def take_turn(self, game: Game):
        self.start_turn()
        self.start_action_phase(game)
        with input_redirect(input="all"):
            self.start_treasure_phase(game)

        if self.state.money >= 8:
            buy_card = "Province"
        elif self.state.money >= 6:
            buy_card = "Gold"
        elif self.state.money >= 3:
            buy_card = "Silver"
        else:
            buy_card = "\n"
        with InputRedirect(input=buy_card):
            self.start_buy_phase(game)

        self.start_cleanup_phase()
