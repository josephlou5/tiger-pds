"""
Adds Bootstrap form styling and validation to field renders.
"""

from wtforms.fields import RadioField, StringField, SubmitField

# ==============================================================================

__all__ = (
    'RadioField',
    'StringField',
    'SubmitField',
)

# ==============================================================================

ERROR_CLASS = 'is-invalid'

# ==============================================================================


def _add_attrs(errors, kwargs, attrs):
    if attrs is None:
        attrs = {}
    # combine attrs
    for key, val in attrs.items():
        existing = kwargs.get(key, '')
        kwargs[key] = f'{val} {existing}'.strip()
    # include bootstrap error class
    if errors:
        existing = kwargs.get('class', '')
        kwargs['class'] = f'{existing} {ERROR_CLASS}'.strip()
    return kwargs


def _add_widget(field_cls, attrs=None, widget=None):

    # inherit from specified widget,
    # or default widget for this field
    class Widget(widget or field_cls.widget.__class__):

        def __call__(self, field, **kwargs):
            if field.description:
                kwargs['aria-describedby'] = field.description_id
            kwargs = _add_attrs(field.errors, kwargs, attrs)
            return super(Widget, self).__call__(field, **kwargs)

    class Field(field_cls):
        widget = Widget()

        @property
        def description_id(self):
            return self.id + '-help'

    return Field


# ==============================================================================

# take care of bootstrap styling in template
RadioField = _add_widget(RadioField)
StringField = _add_widget(StringField, {'class': 'form-control'})
