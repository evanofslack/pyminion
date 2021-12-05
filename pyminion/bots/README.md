## Creating Bots

Pyminion provides a couple of different base classes that can be used to implement new bots. The simpler class is `Bot` found in `base_bot.py`. While this class is capable of playing any card in the base set of Dominion, any card that requires input is not optimized. 

For example, this card can technically play chapel, but it would choose not to trash any cards. It can also play workshop, but it will just gain the first card in the supply that is less than 4 money. Similarly, when facing a discard attack from militia, this bot would just discard the first few cards in its hand. 

When inheriting from this class, it is only necessary to overwrite the `action_priority` and  `buy_priority` methods. This is an example of a bot created from `Bot`:

```python
from pyminion.bots import Bot
from pyminion.game import Game
from pyminion.expansions.base import silver, gold, province, smithy

class BigMoneySmithy(Bot):

    def __init__(
        self,
        player_id: str = "big_money_smithy",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: Game):
        yield smithy

    def buy_priority(self, game: Game):
        money = self.state.money
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money == 4:
            yield smithy
        if money >= 3:
            yield silver
```

The second class that can be used to implement new bots is `OptimizedBot` found in `optimized_bot.py`. This class has some hardcoded logic that dictates how the bot will play certain cards. This class is overall "smarter" than `Bot`. Again, when inheriting from this class, it is only necessary to overwrite the `action_priority` and  `buy_priority` methods but it is also possible to overwrite any of the card specific methods. 

For example, here is a bot based on `OptimizedBot that will buy and play Workshop:

```python
from pyminion.bots import OptimizedBot
from pyminion.core import Card
from pyminion.expansions.base import workshop, duchy, estate, gold, province, silver
from pyminion.game import Game


class WorkshopBot(OptimizedBot):

    def __init__(
        self,
        player_id: str = "workshop_bot",
    ):
        super().__init__(player_id=player_id)

    def action_priority(self, game: Game):
        yield chapel

    def buy_priority(self, game: Game):

        money = self.state.money
        num_workshop = self.get_card_count(card=workshop)

        if num_workshop < 1 and money >= 3:
            yield workshop
        if money >= 8:
            yield province
        if money >= 6:
            yield gold
        if money == 4:
            yield smithy
        if money >= 3:
            yield silver
```

OptimizedBot already defines a method for how workshop will be played:

```python
def workshop(self, game: "Game") -> Card:
    if game.supply.pile_length(pile_name="Province") < 3:
        return estate
    else:
        return silver
```

But we can easily override this method to create a new strategy. We can implement a bot that instead buys Gardens like so:

```python
from pyminion.expansions.base import gardens
class WorkshopBot(OptimizedBot):

    ... # previous code

    def workshop(self, game: "Game") -> Card:
        return gardens
```

To see other implementations of bots please see [/bots/examples](https://github.com/evanofslack/pyminion/tree/master/pyminion/bots/examples)