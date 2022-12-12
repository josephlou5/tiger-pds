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
    # dorm room
    address = Column(String(), nullable=False)
    # name on packages
    name = Column(String())

    def __init__(self, netid, address, name=None):
        self.netid = netid
        self.address = address
        self.name = name
