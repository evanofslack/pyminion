__version__ = "0.2.2"
__author__ = "Evan Slack"


# INITIALIZE LOGGER

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# Create formatter and add to handler
c_format = logging.Formatter("%(message)s")
c_handler.setFormatter(c_format)

# Add handler to the logger
logger.addHandler(c_handler)
