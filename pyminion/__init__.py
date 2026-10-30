__version__ = "0.3.0"
__author__ = "Evan Slack"

import logging

# initialize the package logger with no handler.
# handlers are attached by `Game.play`
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())
