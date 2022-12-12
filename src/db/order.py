"""
order.py
Helper methods for the Orders table.
"""

# ==============================================================================

from db._shared import extract_form_data, query
from db.models import Order, db

# ==============================================================================


def get(order_id):
    """Returns the order with the given id, or None if it doesn't exist.
    """
    return query(Order).filter_by(order_id=order_id).first()


def _get_all(netid):
    return query(Order).filter_by(netid=netid).all()


def get_all(netid):
    """Returns all the pending orders for the given netid."""
    return [o for o in _get_all(netid) if not o.is_delivered]


def get_history(netid):
    """Returns all the delivered orders for the given netid."""
    return [o for o in _get_all(netid) if o.is_delivered]


def _check_existing_order(netid, form, args, order_id=None):
    filters = [
        Order.is_delivered == False,
        Order.netid == netid,
        Order.kiosk == args['kiosk'],
        Order.pin == args['pin'],
    ]
    if order_id is not None:
        filters.append(Order.order_id != order_id)
    # check if a pending order is the same as this one
    existing = query(Order.order_id).filter(*filters).scalar()
    if existing is not None:
        error_msg = 'An order with this kiosk and PIN pair already exists.'
        form.kiosk.errors.append(error_msg)
        form.pin.errors.append(error_msg)
        return True
    return False


def create(netid, user_profile, form):
    """Creates an order with the data from the given FlaskForm.
    Returns True if successful.
    """
    REQUIRED_ARGS = ['kiosk', 'pin']
    OPTIONAL_ARGS = ['alias', 'address', 'name']
    args = extract_form_data(form, REQUIRED_ARGS, OPTIONAL_ARGS)
    print(args)

    if user_profile is None:
        if 'address' not in args:
            form.address.errors.append('No dorm room given in profile.')
            return False
    else:
        # copy values from defaults
        for key in ('address', 'name'):
            if key in args:
                continue
            args[key] = getattr(user_profile, key)

    # check if a pending order is the same as this one
    existing = _check_existing_order(netid, form, args)
    if existing:
        return False

    order = Order(netid, **args)
    db.session.add(order)
    db.session.commit()

    return True


def update(netid, order_id, form):
    """Updates the given order with the data from the given FlaskForm.
    Returns True if successful.
    """
    REQUIRED_ARGS = ['kiosk', 'pin']
    OPTIONAL_ARGS = ['alias', 'address', 'name']
    args = extract_form_data(form, REQUIRED_ARGS, OPTIONAL_ARGS)

    # check if a pending order is the same as this one
    existing = _check_existing_order(netid, form, args, order_id)
    if existing:
        return False

    order = get(order_id)
    changed = False
    for key, value in args.items():
        if getattr(order, key) == value:
            continue
        setattr(order, key, value)
        changed = True
    if not changed:
        return True

    db.session.commit()
    return True


def delete(order_id):
    """Deletes the given order.
    Returns True if successful.
    """
    order = get(order_id)
    if order is None:
        return False
    db.session.delete(order)
    db.session.commit()
    return True
