from pyminion.bots.base_bot import Bot
from pyminion.bots.optimized_bot import OptimizedBot

placeholder = (
    "This keeps isort from moving specific bots above the dependent 'Bot' import"
)

# Specific Bot Implementations
from pyminion.bots.examples.bandit_bot import BanditBot
from pyminion.bots.examples.big_money import BigMoney
from pyminion.bots.examples.big_money_smithy import BigMoneySmithy
from pyminion.bots.examples.big_money_ultimate import BigMoneyUltimate
from pyminion.bots.examples.chapel_bot import ChapelBot
