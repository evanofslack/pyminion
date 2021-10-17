from pyminion.models.base import Card, Turn, Player
from pyminion.exceptions import InsufficientActions


class Victory(Card):
    def __init__(self, name: str, cost: int, victory_points: int):
        super().__init__(name, cost)
        self.victory_points = victory_points


class Treasure(Card):
    def __init__(self, name: str, cost: int, money: int):
        super().__init__(name, cost)
        self.money = money

    def play(self, turn: Turn, player: Player):
        turn.money += self.money
        player.playmat.add(self)
        player.hand.remove(self)


class Action(Card):
    def __init__(self, name: str, cost: int):
        super().__init__(name, cost)

    def play(self):
        """
        Specific play method unique to each action card

        """
        raise NotImplementedError(f"Play method must be implemented for {self.name}")

    def common_play(self, turn: Turn, player: Player):
        """
        Common play method that gets executes for all action cards

        """
        if turn.actions < 1:
            raise InsufficientActions(
                f"{turn.player.player_id}: Not enough actions to play {self.name}"
            )

        player.playmat.add(self)
        player.hand.remove(self)
        turn.actions -= 1


class Smithy(Action):
    def __init__(self, name: str = "Smithy", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        super().common_play(turn, player)

        for i in range(3):  # draw 3 cards from deck and add to hand
            player.hand.add(player.deck.draw())
