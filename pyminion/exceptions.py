class InsufficientActions(Exception):
    """
    Player does not have remaining actions required to play card

    """


class InsufficientMoney(Exception):
    """
    Player does not have enough money to buy card

    """


class InsufficientBuys(Exception):
    """
    Player does not have enough buys to purchase card

    """
