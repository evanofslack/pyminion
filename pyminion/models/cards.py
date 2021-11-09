from pyminion.exceptions import InsufficientActions
from pyminion.models.core import Card, Player


class Victory(Card):
    def __init__(self, name: str, cost: int, type: str):
        super().__init__(name, cost, type)

    def score(self):
        """
        Specific score method unique to each victory card

        """
        raise NotImplementedError(f"Score method must be implemented for {self.name}")


class Treasure(Card):
    def __init__(self, name: str, cost: int, type: str, money: int):
        super().__init__(name, cost, type)
        self.money = money

    def play(self, player: Player):
        """
        Specific play method unique to each treasure card

        """
        raise NotImplementedError(f"Play method must be implemented for {self.name}")


class Action(Card):
    def __init__(
        self, name: str, cost: int, type: str, actions: int, draw: int, money: int
    ):
        super().__init__(name, cost, type)
        self.actions = actions
        self.draw = draw
        self.money = money

    def play(self):
        """
        Specific play method unique to each action card

        """
        raise NotImplementedError(f"play method must be implemented for {self.name}")

    def bot_play(self):
        """
        Specific play method for bots to execute, unique to each action card

        """
        raise NotImplementedError(
            f"bot_play method must be implemented for {self.name}"
        )

    def generic_play(self, player: Player):
        """
        Generic play method that gets executes for all action cards

        """
        if player.state.actions < 1:
            raise InsufficientActions(
                f"{player.player_id}: Not enough actions to play {self.name}"
            )

        player.playmat.add(self)
        player.hand.remove(self)
        player.state.actions -= 1
