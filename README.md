# Pyminion

[![tests](https://github.com/evanofslack/pyminion/actions/workflows/python-app.yml/badge.svg)](https://github.com/evanofslack/pyminion/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/evanofslack/pyminion/branch/master/graph/badge.svg?token=5GW65KFEL5)](https://codecov.io/gh/evanofslack/pyminion)


Pyminion is a library for executing and analyzing games of [Dominion](https://www.riograndegames.com/games/dominion/). At its core, pyminion implements the rules and logic of Dominion and provides an API to interact with the game engine. In addition, it enables interactive games through the command line and simulation of games between bots.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [Support](#support)
-   [Contributing](#contributing)

## Getting Started

Pyminion requires at least Python 3.8 and can easily be installed through pypi

```
python3 -m pip install pyminion
```

## Usage

### Setting up a game

To play an interactive game through the command line against a bot, initialize a human and a bot and assign them as players. Alternatively, games can be created between multiple humans or multiple bots. 

```python
from pyminion.expansions.base import base_set 
from pyminion.game import Game
from pyminion.bots.examples import BigMoney
from pyminion.players import Human

# Initialize human and bot
human = Human()
bot = BigMoney()

# Setup the game
game = Game(players=[human, bot], expansions=[base_set])

# Play game
game.play()

```
### Creating Bots

Defining new bots is relatively straightforward. Inherit from the `Bot` class and implement play and buy strategies in the `action_priority` and `buy_priority` methods respectively.

For example, here is a simple big money + smithy bot:

```python
from pyminion.bots.bot import Bot
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

To see other bot implementations with more advanced decision trees, see [/bots](https://github.com/evanofslack/pyminion/tree/master/pyminion/bots)

### Running Simulations

Simulating multiple games is good metric for determining bot performance. To create a simulation, pass a pyminion game instance into the `Simulator` class and set the number of iterations to be run. 

```python
from pyminion.bots.examples import BigMoney, BigMoneySmithy
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game
from pyminion.simulator import Simulator

bm = BigMoney()
bm_smithy = BigMoneySmithy()

game = Game(players=[bm, bm_smithy], expansions=[base_set], kingdom_cards=[smithy])
sim = Simulator(game, iterations=1000)
sim.run()
```

with the following terminal output: 
```console
~$ python simulation.py
Simulation of 1000 games
big_money wins: 16.8% (168)
big_money_smithy wins: 57.5% (575)
Ties: 25.7% (257)
```
Please see [/examples](https://github.com/evanofslack/pyminion/tree/master/examples) to see demo scripts.  
## Support

Please [open an issue](https://github.com/evanofslack/pyminion/issues/new) for support.

## Contributing

Install this library, test it out, and report any bugs. A welcome contribution would be to create new bots, especially an implementation that uses machine learning to determine optimal play. 

If you would like to contribute, please create a branch, add commits, and [open a pull request](https://github.com/evanofslack/pyminion/pulls).
