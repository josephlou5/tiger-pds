"""
models.py
The database and models.
"""

# ==============================================================================

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String

# ==============================================================================

__all__ = (
    'db',
    'UserProfile',
)

# ==============================================================================

db = SQLAlchemy()

# ==============================================================================


class UserProfile(db.Model):
    """Model for a user's profile."""
    __tablename__ = 'UserProfiles'

    netid = Column(String(), primary_key=True)
    # name on packages
    name = Column(String())
    # dorm room
    address = Column(String(), nullable=False)

    def __init__(self, netid, name=None, address=None):
        self.netid = netid
        self.name = name
        self.address = address
