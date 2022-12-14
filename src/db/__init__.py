"""
__init__.py
Methods and objects pertaining to the database.
"""

# ==============================================================================

from flask_migrate import Migrate

from db import admin, deliverer, order, user_profile
from db.models import db

# ==============================================================================

__all__ = (
    'db',
    'admin',
    'deliverer',
    'user_profile',
    'order',
)

# ==============================================================================


def init_app(app):
    db.init_app(app)
    Migrate(app, db)
