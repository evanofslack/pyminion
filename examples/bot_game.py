"""
Run a single game between two bots. 

"""

from pyminion.bots.examples import BigMoney, BigMoneyUltimate
from pyminion.expansions.base import base_set, smithy
from pyminion.game import Game

bm = BigMoney(player_id="BM")
bm_ultimate = BigMoneyUltimate(player_id="BM_Ultimate")


game = Game(
    players=[bm, bm_ultimate],
    expansions=[base_set],
    kingdom_cards=[smithy],
)

if __name__ == "__main__":
    game.play()
