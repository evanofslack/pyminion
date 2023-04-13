# Creating Bots

Pyminion provides several different base classes that can be used to implement new bots. The goal is to provide a convenient starting point from which new bots can be built.

## `Bot` and `BotDecider`

The first set of classes that can be used are `Bot` and `BotDecider` found in `bot.py`. While these classes are capable of playing any card in the base set of Dominion, cards that require logical input are not optimized.

For example, this card can technically play chapel, but it would choose not to trash any cards. Similarly, when facing a discard attack from militia, this bot would just discard the first few cards in its hand.

When inheriting from `BotDecider`, it is only necessary to overwrite the `action_priority` and  `buy_priority` methods. This is an example of a bot created from `Bot` and `BotDecider`:

```python
from pyminion.bots.bot import Bot, BotDecider
from pyminion.expansions.base import gold, province, silver, smithy
from pyminion.player import Player
from pyminion.game import Game

class BigMoneySmithyDecider(BotDecider):
    """
    Big money + smithy

    """

    def action_priority(self, player: Player, game: Game):
        yield smithy

    def buy_priority(self, player: Player, game: Game):
        money = player.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money == 4:
            yield smithy
        if money >= 3:
            yield silver

class BigMoneySmithy(Bot):
    def __init__(
        self,
        player_id: str = "big_money_smithy",
    ):
        super().__init__(decider=BigMoneySmithyDecider(), player_id=player_id)
```

## `OptimizedBot` and `OptimizedBotDecider`

The second set of classes that can be used to implement new bots are `OptimizedBot` and `OptimizedBotDecider` found in `optimized_bot.py`. These classes have some predefined logic that dictates how the bot will play certain cards. The `OptimizedBotDecider` class is overall "smarter" than `BotDecider`. For example, when this bot plays chapel, it will trash estates (as long as the game isn't close to ending) and will trash copper (as long as it has at least 3 money in its deck). When responding to militia discard attacks, this bot will prioritize discarding victory cards, followed by cheap treasures and actions.

Again, when inheriting from this class, it is only necessary to overwrite the `action_priority` and `buy_priority` methods, but it is also possible to overwrite any of the card specific methods.

For example, here is a bot based on `OptimizedBotDecider` that will buy and play Workshop:

```python
from pyminion.bots.optimized_bot import OptimizedBot, OptimizedBotDecider
from pyminion.expansions.base import workshop, gold, province, silver
from pyminion.player import Player
from pyminion.game import Game

class WorkshopBotDecider(OptimizedBotDecider):
    def action_priority(self, player: Player, game: Game):
        yield workshop

    def buy_priority(self, player: Player, game: Game):
        money = player.state.money
        num_workshop = player.get_card_count(card=workshop)

        if num_workshop < 1 and money >= 3:
            yield workshop
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money >= 3:
            yield silver

class WorkshopBot(OptimizedBot):
    def __init__(
        self,
        player_id: str = "workshop_bot",
    ):
        super().__init__(decider=WorkshopBotDecider(), player_id=player_id)
```

`OptimizedBotDecider` already defines a method for how Workshop will be played:

```python
    def workshop(self, player: "Player", game: "Game") -> Card:
        if game.supply.pile_length(pile_name="Province") < 3:
            return estate
        else:
            return silver
```

But we can easily override this method to create a new strategy. We can implement a bot that instead uses Workshop to gain Gardens:

```python
from pyminion.expansions.base import gardens

class WorkshopBotDecider(OptimizedBotDecider):

    ... # previous code

    def workshop(self, player: "Player", game: "Game") -> Card:
        if gardens in game.supply.available_cards():
            return gardens
        else:
            return silver
```

To see other implementations of bots please see [/bots/examples](https://github.com/evanofslack/pyminion/tree/master/pyminion/bots/examples)
