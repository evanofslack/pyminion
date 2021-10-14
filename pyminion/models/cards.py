from pyminion.models.base import Card, Turn
from pyminion.exceptions import InsufficientActions


class Victory(Card):
    def __init__(self, name: str, cost: int, victory_points: int):
        super().__init__(name, cost)
        self.victory_points = victory_points


class Treasure(Card):
    def __init__(self, name: str, cost: int, money: int):
        super().__init__(name, cost)
        self.money = money

    def play(self, turn: Turn):
        turn.money += self.money
        turn.player.playmat.add(self)
        turn.player.hand.remove(self)


class Action(Card):
    def __init__(self, name: str, cost: int):
        super().__init__(name, cost)

    def play(self):
        """
        Specific play method unique to each action card

        """
        raise NotImplementedError(f"Play method must be implemented for {self.name}")

    def common_play(self, turn: Turn):
        """
        Common play method that gets executes for all action cards

        """
        if turn.actions < 1:
            raise InsufficientActions(
                f"{turn.player.player_id}: Not enough actions to play {self.name}"
            )

        turn.player.playmat.add(self)
        turn.player.hand.remove(self)
        turn.actions -= 1


class Smithy(Action):
    def __init__(self, name: str = "Smithy", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn):
        super().common_play(turn)

        for i in range(3):  # draw 3 cards from deck and add to hand
            turn.player.hand.add(turn.player.deck.draw())
