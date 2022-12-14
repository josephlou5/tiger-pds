"""
admin.py
Helper methods for the Admins table.
"""

# ==============================================================================

from werkzeug.exceptions import BadRequest, Forbidden

from db import deliverer, user
from db._shared import query
from db.models import Admin, db

# ==============================================================================


def get_all():
    """Returns all the admin netids as a set."""
    return set(admin.netid for admin in query(Admin).all())


def get_all_users(admin_netid):
    """Returns all the users, along with their permissions, as a list of
    dicts. `admin_netid` must be an admin.

    Returns the users in order of admin, deliverers, and regular users.
    """
    check(admin_netid)

    def _make(netid):
        return {
            'netid': netid,
            'is_admin': False,
            'is_deliverer': False,
        }

    users = {}
    for netid in get_all():
        if netid not in users:
            users[netid] = _make(netid)
        users[netid]['is_admin'] = True
    for netid in deliverer.get_all(admin_netid):
        if netid not in users:
            users[netid] = _make(netid)
        users[netid]['is_deliverer'] = True
    for netid in user.get_all(admin_netid):
        if netid not in users:
            users[netid] = _make(netid)
    return list(users.values())


def _get(netid):
    return query(Admin).filter_by(netid=netid).first()


def is_admin(netid):
    """Returns True if the given netid is an admin."""
    return _get(netid) is not None


def check(netid):
    """Checks that the given netid is an admin.
    Raises errors for invalid permissions.
    """
    if not is_admin(netid):
        raise Forbidden('You do not have permission to view an admin page.')


def _add(netid):
    admin = Admin(netid)
    db.session.add(admin)
    db.session.commit()


def add_first(netid):
    """Adds the given netid as the first admin.
    Returns True if successful.
    """
    if len(get_all()) > 0:
        raise BadRequest('You cannot be the first admin; '
                         'there are already existing admins.')
    _add(netid)
    return True


def add(admin_netid, netid):
    """Adds the given netid as an admin. `admin_netid` must be an admin.
    Returns True if successful.
    """
    check(admin_netid)
    if is_admin(netid):
        return True
    _add(netid)
    return True


def delete(admin_netid, netid):
    """Deletes the given netid as an admin. `admin_netid` must be an
    admin.
    Returns True if successful.
    """
    check(admin_netid)
    admin = _get(netid)
    if admin is None:
        return True
    db.session.delete(admin)
    db.session.commit()
    return True
