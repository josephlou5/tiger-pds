"""
_shared.py
Shared methods for working with the database.
"""

# ==============================================================================

from db.models import db

# ==============================================================================


def extract_form_data(form, required=None, optional=None):
    if required is None:
        required = []
    if optional is None:
        optional = []

    args = {}
    for key in required:
        args[key] = form.data[key]
    for key in optional:
        if not form.data[key]:
            continue
        args[key] = form.data[key]
    return args


# ==============================================================================


def query(model):
    return db.session.query(model)
