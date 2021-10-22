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


class InvalidInput(Exception):
    """
    Base class for input exceptions

    """


class InvalidBinaryInput(InvalidInput):
    """
    Invalid response, valid choices are "y" or "n"

    """


class InvalidMultiCardInput(InvalidInput):
    """
    Invalid response, that input cannot be discarded

    """
