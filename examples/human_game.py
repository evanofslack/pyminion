"""
Play a game through the terminal.
Either by yourself, with another human, or against a bot.

"""

from pyminion.bots.examples import BigMoney
from pyminion.expansions.base import artisan, bandit, base_set, witch
from pyminion.expansions.intrigue import intrigue_set, nobles, bridge
from pyminion.game import Game
from pyminion.human import Human

human = Human(player_id="Human")
bm = BigMoney(player_id="Big Money")

game = Game(
    players=[human, bm],
    expansions=[base_set, intrigue_set],
    kingdom_cards=[artisan, bandit, witch, nobles, bridge],  # specific cards to add to the kingdom
    random_order=True,  # players start in random order
)

if __name__ == "__main__":
    result = game.play()
