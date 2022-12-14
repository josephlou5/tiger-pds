"""
models.py
The database and models.
"""

# ==============================================================================

from datetime import datetime

import pytz
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, Integer, String

# ==============================================================================

__all__ = (
    'db',
    'Deliverer',
    'UserProfile',
    'Order',
)

# ==============================================================================

UTC_TZ = pytz.utc
EASTERN_TZ = pytz.timezone('US/Eastern')

# ==============================================================================

db = SQLAlchemy()

# ==============================================================================


class Admin(db.Model):
    """Model for a site admin."""
    __tablename__ = 'Admins'

    netid = Column(String(), primary_key=True)

    def __init__(self, netid):
        self.netid = netid


class Deliverer(db.Model):
    """Model for users who do deliveries."""
    __tablename__ = 'Deliverers'

    netid = Column(String(), primary_key=True)

    def __init__(self, netid):
        self.netid = netid


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


class Order(db.Model):
    """Model for an order."""
    __tablename__ = 'Orders'

    order_id = Column(Integer, primary_key=True)

    # the person the order belongs to
    netid = Column(String(), nullable=False)
    # an alias for the package (private)
    alias = Column(String())
    # the locker kiosk (103 A - 109 P)
    kiosk = Column(String(5), nullable=False)
    # the 6-digit pin number to unlock the package locker
    pin = Column(String(6), nullable=False)

    # the delivery location
    address = Column(String(), nullable=False)
    # the name on the package
    name = Column(String())

    # the person who delivered the order
    delivery_netid = Column(String)
    # whether the package has been delivered
    is_delivered = Column(Boolean(), default=False, nullable=False)
    # the date the package was delivered to the address
    date_delivered = Column(DateTime(timezone=False))

    date_created = Column(DateTime(timezone=False),
                          default=datetime.utcnow,
                          nullable=False)

    def __init__(self, netid, kiosk, pin, address, alias=None, name=None):
        self.netid = netid
        self.alias = alias
        self.kiosk = kiosk
        self.pin = pin
        self.address = address
        self.name = name

    @property
    def order_title(self):
        if self.alias:
            return self.alias
        return f'Order at Kiosk {self.kiosk}'

    def _date_delivered_fmt(self, fmt_str):
        dt_utc = UTC_TZ.localize(self.date_delivered)
        dt_local = dt_utc.astimezone(EASTERN_TZ)
        return dt_local.strftime(fmt_str)

    @property
    def order_status(self):
        if self.is_delivered:
            if self.date_delivered is None:
                return 'Delivered'
            date_delivered_str = self._date_delivered_fmt(
                '%a, %b %-d, %Y, %H:%M')
            return f'Delivered on {date_delivered_str}'
        if self.delivery_netid:
            return 'Picked up from Frist'
        return 'Waiting to be picked up from Frist'

    @property
    def order_status_admin(self):
        if self.is_delivered:
            missing = []
            delivery_str = 'Delivered'
            if self.date_delivered is not None:
                delivery_str += ' at ' + self._date_delivered_fmt(
                    '%Y-%m-%d %H:%M')
            else:
                missing.append('date')
            if self.delivery_netid is not None:
                delivery_str += ' by ' + self.delivery_netid
            else:
                missing.append('netid')
            if len(missing) > 0:
                delivery_str += ' (missing ' + ' and '.join(missing) + ')'
            return delivery_str
        if self.delivery_netid:
            return 'Claimed by ' + self.delivery_netid
        return 'Unclaimed'
