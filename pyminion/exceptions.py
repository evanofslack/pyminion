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


class EmptyPile(Exception):
    """
    The pile does is empty

    """


class PileNotFound(Exception):
    """
    The pile does not exist

    """


class InvalidBinaryInput(Exception):
    """
    Invalid response, valid choices are "y" or "n"

    """
