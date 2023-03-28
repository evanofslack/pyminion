import logging
from typing import TYPE_CHECKING, List, Optional, Union

from pyminion.core import (CardType, Card, Deck)
from pyminion.decisions import (binary_decision, multiple_card_decision,
                                single_card_decision, validate_input)
from pyminion.exceptions import (InsufficientMoney, InvalidBinaryInput,
                                 InvalidMultiCardInput, InvalidSingleCardInput)
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class HumanDecider:
    """
    Prompts human for decisions through the terminal.

    """

    @validate_input(exceptions=InvalidBinaryInput)
    def binary_decision(
        self,
        prompt: str,
        card: Card,
        player: "Player",
        game: "Game",
        relevant_cards: Optional[List[Card]] = None,
    ) -> bool:
        """
        Wrap binary_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return binary_decision(prompt=prompt)


class Human(Player):
    """
    Human player can make choices as to which cards
    to play and buy in real time through the terminal

    """

    def __init__(
        self,
        deck: Optional[Deck] = None,
        player_id: str = "human",
    ):
        super().__init__(decider=HumanDecider(), deck=deck, player_id=player_id)

    @staticmethod
    @validate_input(exceptions=InvalidSingleCardInput)
    def single_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[Union[Card, str]]:
        """
        Wrap single_card_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """

        return single_card_decision(prompt=prompt, valid_cards=valid_cards)

    @staticmethod
    @validate_input(exceptions=InvalidMultiCardInput)
    def multiple_card_decision(
        prompt: str,
        valid_cards: List[Card],
    ) -> Optional[List[Card]]:
        """
        Wrap multiple_card_decision with @validate_input decorator to
        repeat prompt if input is invalid.

        """
        return multiple_card_decision(prompt=prompt, valid_cards=valid_cards)

    def is_attacked(self, player: Player, attack_card: Card, game: "Game") -> bool:
        for card in self.hand.cards:
            if card.name == "Moat":
                block = self.decider.binary_decision(
                    prompt=f"Would you like to block {player.player_id}'s {attack_card} with your Moat? y/n: ",
                    card=card,
                    player=self,
                    game=game,
                    relevant_cards=[attack_card],
                )
                return not block
        return True

    def start_action_phase(self, game: "Game") -> None:
        while self.state.actions:

            viable_actions = [card for card in self.hand.cards if CardType.Action in card.type]
            if not viable_actions:
                return

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_action(game: "Game") -> None:
                logger.info(f"Hand: {self.hand}")
                card = single_card_decision(
                    prompt="Choose an action card to play: ",
                    valid_cards=viable_actions,
                )
                if not card or isinstance(card, str):
                    return
                self.play(card, game)
                return

            choose_action(game)

    def start_treasure_phase(self, game: "Game") -> None:
        viable_treasures = [card for card in self.hand.cards if CardType.Treasure in card.type]
        while viable_treasures:

            @validate_input(exceptions=InvalidSingleCardInput)
            def choose_treasure(game: "Game") -> None:
                logger.info(f"Hand: {self.hand}")
                response = single_card_decision(
                    prompt="Choose an treasure card to play or 'all' to autoplay treasures: ",
                    valid_cards=viable_treasures,
                    valid_mixin="all",
                )
                if response == "all":
                    self.autoplay_treasures(
                        viable_treasures=viable_treasures, game=game
                    )
                    return
                if not response or isinstance(response, str):
                    return
                self.exact_play(response, game)
                logger.info(f"{self.player_id} played {response}")
                viable_treasures.remove(response)

            choose_treasure(game)

    def start_buy_phase(self, game: "Game") -> None:
        while self.state.buys:
            logger.info(f"\nSupply:{game.supply}")
            logger.info(f"Money: {self.state.money}")
            logger.info(f"Buys: {self.state.buys}")

            @validate_input(exceptions=(InvalidSingleCardInput, InsufficientMoney))
            def choose_buy(game: "Game") -> None:
                card = single_card_decision(
                    prompt="Choose a card to buy: ",
                    valid_cards=game.supply.avaliable_cards(),
                )
                if not card or isinstance(card, str):
                    return
                self.buy(card, game.supply)

            choose_buy(game)

    def take_turn(self, game: "Game") -> None:
        self.start_turn()
        logger.info(f"\nTurn {self.turns} - {self.player_id}")
        self.start_action_phase(game)
        self.start_treasure_phase(game)
        self.start_buy_phase(game)
        self.start_cleanup_phase()
