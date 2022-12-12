"""
__init__.py
The FlaskForm objects.
"""

# ==============================================================================

from forms.edit_order_form import EditOrderForm
from forms.edit_profile_form import EditProfileForm

# ==============================================================================

__all__ = (
    'EditOrderForm',
    'EditProfileForm',
)
