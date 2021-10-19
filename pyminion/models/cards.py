from pyminion.models.base import Card, Turn, Player, Trash
from pyminion.exceptions import InsufficientActions, InvalidBinaryInput
from pyminion.base_set.base_cards import copper


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
        Generic play method that gets executes for all action cards

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
        """
        +3 cards

        """
        super().common_play(turn, player)

        for i in range(3):
            player.draw()


class Village(Action):
    def __init__(self, name: str = "Village", cost: int = 3):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +1 card, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 2
        player.draw()


class Laboratory(Action):
    def __init__(self, name: str = "Laboratory", cost: int = 5):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +2 cards, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        player.draw()


class Laboratory(Action):
    def __init__(self, name: str = "Laboratory", cost: int = 5):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +2 cards, +1 action

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        player.draw()


class Market(Action):
    def __init__(self, name: str = "Market", cost: int = 5):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player):
        """
        +1 card, +1 action, +1 money, +1 buy

        """
        super().common_play(turn, player)
        turn.actions += 1
        player.draw()
        turn.money += 1
        turn.buys += 1


class Moneylender(Action):
    def __init__(self, name: str = "Moneylender", cost: int = 4):
        super().__init__(name, cost)

    def play(self, turn: Turn, player: Player, trash: Trash):
        """
        You may trash a copper from your hand for + 3 money

        """
        super().common_play(turn, player)
        if copper in player.hand.cards:
            decision = input("Do you want to trash a copper from your hand? y/n?")
            if decision == "y":
                player.trash(target_card=copper, trash=trash)
                turn.money += 3
            elif decision == "n":
                pass
            else:
                raise InvalidBinaryInput
