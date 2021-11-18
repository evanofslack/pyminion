"""
pyminion

Dominion but make it Python

"""

__version__ = "0.1.5"
__author__ = "Evan Slack"


# INITIALIZE LOGGER

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("game.log", mode="w")
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter("%(message)s")
f_format = logging.Formatter("%(message)s")
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
