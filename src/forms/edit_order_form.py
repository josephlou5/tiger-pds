"""
edit_order_form.py
The FlaskForm for editing an order.
"""

# ==============================================================================

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError

from forms.wtforms_bootstrap import RadioField, StringField, SubmitField

# ==============================================================================

ALIAS_DESCRIPTION = (
    'An optional name of this package, for your convenience. This will '
    'not be shared with anyone.')
KIOSK_DESCRIPTION = ('The locker kiosk that your package is in.')
PIN_DESCRIPTION = ('The 6-digit PIN number to unlock the locker.')
NAME_DESCRIPTION = (
    'The name on this package, if it is different from the name on '
    'your profile. Used to confirm the package is for you.')
ADDRESS_DESCRIPTION = (
    'The room to deliver this packages to, if it is different from the '
    'room on your profile.')

# ==============================================================================

# yapf: disable
KIOSK_CHOICES = [
    '103 A', '103 B', '103 C', '103 D',
    '104 E', '104 F', '104 G', '104 H',
    '107 I', '107 J', '107 K', '107 L',
    '108 M', '108 N', '108 O', '108 P',
]
# yapf: enable

# ==============================================================================


class EditOrderForm(FlaskForm):
    alias = StringField('Package Name', description=ALIAS_DESCRIPTION)
    kiosk = RadioField(
        'Locker Kiosk',
        description=KIOSK_DESCRIPTION,
        choices=KIOSK_CHOICES,
        validators=[InputRequired('Please select the locker kiosk.')])
    pin = StringField(
        'PIN Number',
        description=PIN_DESCRIPTION,
        validators=[InputRequired('Please enter the PIN number.')])

    name = StringField('Name on package', description=NAME_DESCRIPTION)
    address = StringField('Deliver to', description=ADDRESS_DESCRIPTION)

    submit = SubmitField('Save')
    delete = SubmitField('Delete Order')

    def validate_pin(form, field):
        pin = field.data
        if not pin.isdigit():
            raise ValidationError('The PIN must be a number.')
        if len(pin) != 6:
            # is it bad to hardcode something like this? what if it
            # changes in the future?
            raise ValidationError('The PIN number must be 6 digits.')

    def kiosk_groups(self, group_size):
        num_left = len(KIOSK_CHOICES)
        kiosk_choices = iter(self.kiosk)
        while num_left > 0:
            group = []
            for _ in range(group_size):
                try:
                    group.append(next(kiosk_choices))
                    num_left -= 1
                except StopIteration:
                    break
            yield group
