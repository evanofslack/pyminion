"""
Run a single game between two bots.

Here we do not log the game to console.
Instead, we save the game output to a file (pyminion.log).
We only print the result of the game to console.

"""

from pyminion.bots.examples import BigMoney, BigMoneyUltimate
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game

bm = BigMoney(player_id="BM")
bm_ultimate = BigMoneyUltimate(player_id="BM_Ultimate")


game = Game(
    players=[bm, bm_ultimate],
    expansions=[base_set],
    kingdom_cards=[smithy],  # specific cards to add to the kingdom
    random_order=True,  # players start in random order
    log_stdout=False,  # log the output to stdout
    log_file=True,  # log the output to file
    log_file_name="pyminion.log",  # name of file to log output
)

if __name__ == "__main__":
    result = game.play()
    print(result)
