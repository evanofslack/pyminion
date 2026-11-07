import importlib.metadata
import logging

__version__ = importlib.metadata.version(__name__)
__author__ = "Evan Slack"

# initialize the package logger with no handler.
# handlers are attached by `Game.play`
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())
