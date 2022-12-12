"""
user_profile.py
Helper methods for the UserProfiles table.
"""

# ==============================================================================

from werkzeug.exceptions import Forbidden

from db._shared import extract_form_data, query
from db.models import UserProfile, db

# ==============================================================================


def get(netid):
    """Returns the profile for the given netid, or None if it doesn't
    exist.
    """
    return query(UserProfile).filter_by(netid=netid).first()


def check_does_delivery(netid):
    """Checks if the user is authorized to do deliveries.
    Raises errors for invalid permissions.
    """
    profile = get(netid)
    if profile is None or not profile.does_delivery:
        raise Forbidden('You do not have permission to make deliveries.')


def save(netid, form):
    """Creates or updates the profile for the given netid with the data
    from the given FlaskForm.
    Returns True if successful.
    """
    REQUIRED_ARGS = ['address']
    OPTIONAL_ARGS = ['name']
    args = extract_form_data(form, REQUIRED_ARGS, OPTIONAL_ARGS)

    profile = get(netid)
    if profile is None:
        # creating
        profile = UserProfile(netid, **args)
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
