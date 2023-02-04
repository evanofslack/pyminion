"""
Play a game through the terminal. Either by yourself, with another human, or against a bot.

"""

from pyminion.bots.examples import BigMoney
from pyminion.expansions.base import artisan, bandit, base_set, witch
from pyminion.game import Game
from pyminion.players import Human

human = Human(player_id="Human")
bm = BigMoney(player_id="Big Moneu")

game = Game(
    players=[human, bm],
    expansions=[base_set],
    kingdom_cards=[artisan, bandit, witch],
    use_logger=True,
    log_file_name="pyminion.log",
)

if __name__ == "__main__":
    result = game.play()
