"""
deliverer.py
Helper methods for the Deliverers table.
"""

# ==============================================================================

from werkzeug.exceptions import Forbidden

from db import admin
from db._shared import query
from db.models import Deliverer, db

# ==============================================================================


def get_all(admin_netid):
    """Returns all the deliverer netids as a set. `admin_netid` must be
    an admin.
    """
    admin.check(admin_netid)
    return set(user.netid for user in query(Deliverer).all())


def _get(netid):
    return query(Deliverer).filter_by(netid=netid).first()


def is_deliverer(netid):
    """Returns True if the given netid is a deliverer."""
    return _get(netid) is not None


def check(netid):
    """Checks if the given netid is a deliverer.
    Raises errors for invalid permissions.
    """
    if not is_deliverer(netid):
        raise Forbidden('You do not have permission to make deliveries.')


def add(admin_netid, netid):
    """Adds the given netid as a deliverer. `admin_netid` must be an
    admin.
    Returns True if successful.
    """
    admin.check(admin_netid)
    if is_deliverer(netid):
        return True
    deliverer = Deliverer(netid)
    db.session.add(deliverer)
    db.session.commit()
    return True


def delete(admin_netid, netid):
    """Deletes the given netid as a deliverer. `admin_netid` must be an
    admin.
    Returns True if successful.
    """
    admin.check(admin_netid)
    deliverer = _get(netid)
    if deliverer is None:
        return True
    db.session.delete(deliverer)
    db.session.commit()
    return True
