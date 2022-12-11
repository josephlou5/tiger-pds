"""
config.py
Defines configuration objects for the Flask server.
"""

# ==============================================================================

import os

try:
    from keys import DEV_POSTGRES_PASSWORD, DEV_SECRET_KEY
except ImportError:
    DEV_SECRET_KEY = None
    DEV_POSTGRES_PASSWORD = None

# ==============================================================================


class Config:
    """The base config object."""
    DEBUG = False
    DEVELOPMENT = False

    SECRET_KEY = 'secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """The config object for production."""
    SECRET_KEY = os.environ.get('PROD_SECRET_KEY')

    if os.getenv('SQLALCHEMY_DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI').replace(
            'postgres://', 'postgresql://', 1)
    else:
        SQLALCHEMY_DATABASE_URI = None


class DevConfig(Config):
    """The config object for development."""
    DEBUG = True
    DEVELOPMENT = True

    SECRET_KEY = DEV_SECRET_KEY

    SQLALCHEMY_DATABASE_URI = \
        'postgresql://{username}:{password}@{server}:{port}/{db_name}'.format(
            username='postgres',
            password=DEV_POSTGRES_PASSWORD,
            server='localhost',
            port=5432,
            db_name='tiger-pds-dev')


# ==============================================================================


def get_config(debug=False):
    if debug:
        return DevConfig
    return ProdConfig
