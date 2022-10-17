"""
config.py
Defines configuration objects for the Flask server.
"""

# ==============================================================================

import os

try:
    from keys import DEV_SECRET_KEY
except ImportError:
    DEV_SECRET_KEY = None

# ==============================================================================


class Config:
    """The default config object."""
    DEBUG = False
    DEVELOPMENT = False

    SECRET_KEY = 'secret'


# ==============================================================================


class ProdConfig(Config):
    """The config object for production."""
    SECRET_KEY = os.environ.get('PROD_SECRET_KEY')


# ==============================================================================


class DevConfig(Config):
    """The config object for development."""
    DEBUG = True
    DEVELOPMENT = True

    SECRET_KEY = DEV_SECRET_KEY
