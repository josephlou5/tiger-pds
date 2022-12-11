"""
edit_profile_form.py
The FlaskForm for editing a user's profile.
"""

# ==============================================================================

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

from forms.wtforms_bootstrap import StringField, SubmitField

# ==============================================================================

NAME_DESCRIPTION = (
    'The name on your packages, if you would like the deliverer to '
    'confirm the package is for you.')
ADDRESS_DESCRIPTION = ('The room to deliver your packages to.')

# ==============================================================================


class EditProfileForm(FlaskForm):
    name = StringField('Name on packages', description=NAME_DESCRIPTION)
    # TODO: may want to be able to validate the dorm rooms, but that
    # would require a lot of work. alternatively, could use a dropdown
    # list with all the rooms.
    address = StringField(
        'Dorm room',
        description=ADDRESS_DESCRIPTION,
        validators=[InputRequired('Please enter your dorm room.')])

    submit = SubmitField('Save')
