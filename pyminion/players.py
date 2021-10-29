from pyminion.models.core import Player, Deck, Game
from pyminion.expansions.base import silver, gold, province, smithy
from pyminion.decisions import single_card_decision, validate_input
from pyminion.exceptions import InvalidSingleCardInput, InsufficientMoney


class Human(Player):
    """
    Human player can make choices as to which cards
    to play and buy in real time through the terminal

    """

    def __init__(
        self,
        deck: Deck,
        player_id: str = "human",
    ):
        super().__init__(deck=deck, player_id=player_id)

    @validate_input(exceptions=InvalidSingleCardInput)
    def choose_action(self, game: Game) -> bool:
        print(self.hand)
        card = single_card_decision(
            prompt="Choose an action card to play: ",
            valid_cards=self.hand.cards,
        )
        if not card:
            return False
        self.play(card, game)
        print(f"{self.player_id} played {card}")
        return True

    @validate_input(exceptions=(InvalidSingleCardInput, InsufficientMoney))
    def choose_buy(self, game: Game) -> bool:
        card = single_card_decision(
            prompt="Choose a card to buy: ",
            valid_cards=game.supply.avaliable_cards(),
        )
        if not card:
            return False
        self.buy(card, game.supply)
        print(f"{self.player_id} bought {card}")
        return True

    def take_turn(self, game: Game) -> None:
        self.start_turn()
        print("\nTurn: ", self.turns)
        play_actions = True
        while play_actions:
            print("Actions: ", self.state.actions)
            play_actions = self.choose_action(game)
            if self.state.actions < 1:
                break
        self.autoplay_treasures()
        make_buys = True
        while make_buys:
            print("\nMoney: ", self.state.money)
            print("Buys: ", self.state.buys)
            make_buys = self.choose_buy(game)
            if self.state.buys < 1:
                break
        self.cleanup()


class BigMoney(Player):
    """
    Only buys money and provinces

    """

    def __init__(
        self,
        deck: Deck,
        player_id: str = "big_money",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def take_turn(self, game: Game):
        self.start_turn()

        self.autoplay_treasures()
        if self.state.money >= 8:
            self.buy(province, game.supply)
        elif self.state.money >= 6:
            self.buy(gold, game.supply)
        elif self.state.money >= 3:
            self.buy(silver, game.supply)
        self.cleanup()


class BM_Smithy(Player):
    """
    Same as big money except tries to buy and play smithy too

    """

    def __init__(
        self,
        deck: Deck,
        player_id: str = "bm_smithy",
    ):
        super().__init__(deck=deck, player_id=player_id)

    def take_turn(self, game: Game):

        self.start_turn()

        try:
            self.play(smithy, game)
        except:
            pass

        self.autoplay_treasures()
        if self.state.money >= 8:
            self.buy(province, game.supply)
        elif self.state.money >= 6:
            self.buy(gold, game.supply)
        elif self.state.money >= 4:
            self.buy(smithy, game.supply)
        elif self.state.money >= 3:
            self.buy(silver, game.supply)
        self.cleanup()
