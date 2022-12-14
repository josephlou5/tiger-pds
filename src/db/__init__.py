"""
__init__.py
Methods and objects pertaining to the database.
"""

# ==============================================================================

from flask_migrate import Migrate

from db import admin, deliverer, order, user
from db.models import db

# ==============================================================================

__all__ = (
    'db',
    'admin',
    'deliverer',
    'order',
    'user',
)

# ==============================================================================


def init_app(app):
    db.init_app(app)
    Migrate(app, db)
