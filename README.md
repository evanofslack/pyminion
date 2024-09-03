# Pyminion

[![tests](https://github.com/evanofslack/pyminion/actions/workflows/python-app.yml/badge.svg)](https://github.com/evanofslack/pyminion/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/evanofslack/pyminion/branch/master/graph/badge.svg?token=5GW65KFEL5)](https://codecov.io/gh/evanofslack/pyminion)

<img width="800" alt="pyminion-logo" src="https://github.com/evanofslack/pyminion/assets/51209817/85e6ed9f-8cbf-4781-9c0b-f29c1d0a2162">
<br></br>

Pyminion is a library for executing and analyzing games of [Dominion](https://www.riograndegames.com/games/dominion/).
At its core, pyminion implements the rules and logic of Dominion and provides
an API to interact with the game engine. In addition, it enables interactive
games through the command line and simulation of games between bots.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Installation

Pyminion requires at least Python 3.10 and can easily be installed through pypi

```bash
python3 -m pip install pyminion
```

## Usage

### Setting up a game

To play an interactive game through the command line against a bot, initialize
a human and a bot and assign them as players. Alternatively, games can be
created between multiple humans or multiple bots.

```python
from pyminion.expansions import base, intrigue, seaside, alchemy
from pyminion.game import Game
from pyminion.bots.examples import BigMoney
from pyminion.human import Human

# Initialize human and bot
human = Human()
bot = BigMoney()

# Setup the game
game = Game(players=[human, bot], expansions=[base.base_set, intrigue.intrigue_set, seaside.seaside_set, alchemy.alchemy_set])

# Play game
game.play()

```

### Creating Bots

Defining new bots is relatively straightforward. Inherit from the
`BotDecider` class and implement play and buy strategies in the
`action_priority` and `buy_priority` methods respectively.

For example, here is a simple big money + smithy bot:

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

To see other bot implementations with more advanced decision trees, see [/bots](https://github.com/evanofslack/pyminion/tree/master/pyminion/bots)

### Running Simulations

Simulating multiple games is good metric for determining bot performance.
To create a simulation, pass a pyminion game instance into the `Simulator`
class and set the number of iterations to be run.

```python
from pyminion.bots.examples import BigMoney, BigMoneySmithy
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game
from pyminion.simulator import Simulator

bm = BigMoney()
bm_smithy = BigMoneySmithy()

game = Game(players=[bm, bm_smithy], expansions=[base_set], kingdom_cards=[smithy], log_stdout=False)
sim = Simulator(game, iterations=1000)
result = sim.run()
print(result)
```

with the following terminal output:

```console
~$ python simulation.py
Simulation Result: ran 1000 games
big_money won 110, lost 676, tied 214
big_money_smithy won 676, lost 110, tied 214
```

Please see [/examples](https://github.com/evanofslack/pyminion/tree/master/examples) to see demo scripts.

## Support

Please [open an issue](https://github.com/evanofslack/pyminion/issues/new) for support.

## Contributing

Install this library, test it out, and report any bugs. A welcome contribution
would be to create new bots, especially an implementation that uses machine
learning to determine optimal play.

If you would like to contribute, please create a branch, add commits, and
[open a pull request](https://github.com/evanofslack/pyminion/pulls).
