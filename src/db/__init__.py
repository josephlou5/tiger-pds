"""
__init__.py
Methods and objects pertaining to the database.
"""

# ==============================================================================

from flask_migrate import Migrate

from db import user_profile
from db.models import db

# ==============================================================================

__all__ = (
    'db',
    'user_profile',
)

# ==============================================================================


def init_app(app):
    db.init_app(app)
    Migrate(app, db)
