"""
user.py
Helper methods for the Users table.
"""

# ==============================================================================

from db import admin
from db._shared import extract_form_data, query
from db.models import User, db

# ==============================================================================


def get_all(admin_netid):
    """Returns all the user netids as a set. `admin_netid` must be an
    admin.
    """
    admin.check(admin_netid)
    return set(user.netid for user in query(User).all())


def get(netid):
    """Returns the user with the given netid, or None if it doesn't
    exist.
    """
    return query(User).filter_by(netid=netid).first()


def add(admin_netid, netid):
    """Adds the given netid as a user. `admin_netid` must be an admin.
    Returns True if successful.
    """
    admin.check(admin_netid)
    if get(netid) is not None:
        return True
    user = User(netid)
    db.session.add(user)
    db.session.commit()
    return True


def save(netid, form):
    """Creates or updates the user's profile for the given netid with
    the data from the given FlaskForm.
    Returns True if successful.
    """
    REQUIRED_ARGS = []
    OPTIONAL_ARGS = ['address', 'name']
    args = extract_form_data(form, REQUIRED_ARGS, OPTIONAL_ARGS)

    profile = get(netid)
    if profile is None:
        # creating
        profile = User(netid, **args)
        db.session.add(profile)
    else:
        # updating
        changed = False
        for key, value in args.items():
            if getattr(profile, key) == value:
                continue
            setattr(profile, key, value)
            changed = True
        if not changed:
            return True

    db.session.commit()
    return True
