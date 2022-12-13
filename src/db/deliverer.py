"""
deliverer.py
Helper methods for the Deliverers table.
"""

# ==============================================================================

from werkzeug.exceptions import Forbidden

from db._shared import query
from db.models import Deliverer, db

# ==============================================================================


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


def add(netid):
    """Adds the given netid as a deliverer.
    Returns True if successful.
    """
    if is_deliverer(netid):
        return True
    deliverer = Deliverer(netid)
    db.session.add(deliverer)
    db.session.commit()
    return True


def remove(netid):
    """Removes the given netid as a deliverer.
    Returns True if successful.
    """
    if not is_deliverer(netid):
        return True
    deliverer = _get(netid)
    db.session.delete(deliverer)
    db.session.commit()
    return True
