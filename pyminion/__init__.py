__version__ = "0.2.2"
__author__ = "Evan Slack"

import logging

# initalize logger with no handler.
# handlers are added in the `Game` init
logger = logging.getLogger()
logger.setLevel((logging.INFO))
logger.addHandler(logging.NullHandler())
