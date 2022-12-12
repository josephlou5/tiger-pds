"""
user_profile.py
Helper methods for the UserProfiles table.
"""

# ==============================================================================

from db.models import UserProfile, db

# ==============================================================================


def get(netid):
    """Returns the profile for the given netid, or None if it doesn't
    exist.
    """
    return db.session.query(UserProfile).filter(
        UserProfile.netid == netid).first()


def save(netid, form):
    """Creates or updates the profile for the given netid with the data
    from the given FlaskForm.
    Returns True if successful.
    """

    args = {}
    for key in ('name', 'address'):
        if key not in form.data:
            continue
        args[key] = form.data[key]

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
