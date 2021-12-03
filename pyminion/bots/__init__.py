from pyminion.bots.abstract_bot import AbstractBot
from pyminion.bots.base_bot import Bot
from pyminion.bots.optimized_bot import OptimizedBot

placeholder = (
    "This keeps isort from moving specific bots above the dependent 'Bot' import"
)

# Specific Bot Implementations
from pyminion.bots.bandit_bot import BanditBot
from pyminion.bots.big_money import BigMoney
from pyminion.bots.big_money_smithy import BigMoneySmithy
from pyminion.bots.big_money_ultimate import BigMoneyUltimate
from pyminion.bots.chapel_bot import ChapelBot
