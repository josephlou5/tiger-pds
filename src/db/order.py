"""
order.py
Helper methods for the Orders table.
"""

# ==============================================================================

from datetime import datetime

from werkzeug.exceptions import Forbidden, NotFound

from db import admin, deliverer
from db._shared import extract_form_data, query
from db.models import Order, db

# ==============================================================================


def get(order_id, netid=None, action='view'):
    """Returns the order with the given id.
    If the netid is given, also make sure the user has permission to
    retrieve this order.
    """
    order = query(Order).filter_by(order_id=order_id).first()
    if order is None:
        raise NotFound(f'Order {order_id} could not be found.')
    if netid is None:
        # no need to validate netid
        pass
    elif admin.is_admin(netid):
        # admins can get any order
        pass
    elif netid != order.netid:
        raise Forbidden(f'You do not have permission to {action} this order.')
    return order


def get_all_orders(netid):
    """Returns all the orders. The netid must be an admin."""
    admin.check(netid)
    return query(Order).all()


def get_all(netid):
    """Returns all the pending orders and previous orders for the given
    netid.
    """
    orders = query(Order).filter_by(netid=netid).all()
    pending = []
    history = []
    for order in orders:
        if order.is_delivered:
            history.append(order)
        else:
            pending.append(order)
    return pending, history


def get_delivering(netid):
    """Returns all the orders the given netid is currently delivering.
    """
    deliverer.check(netid)
    filters = {
        'is_delivered': False,
        'delivery_netid': netid,
    }
    return query(Order).filter_by(**filters).all()


def get_needs_delivery(netid):
    """Returns all the orders needing delivery."""
    deliverer.check(netid)
    filters = {
        'is_delivered': False,
        'delivery_netid': None,
    }
    return query(Order).filter_by(**filters).all()


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


def create(netid, profile, form):
    """Creates an order with the data from the given FlaskForm.
    Returns True if successful.
    """
    REQUIRED_ARGS = ['kiosk', 'pin']
    OPTIONAL_ARGS = ['alias', 'address', 'name']
    args = extract_form_data(form, REQUIRED_ARGS, OPTIONAL_ARGS)

    if profile is None:
        if 'address' not in args:
            form.address.errors.append('No dorm room given in profile.')
            return False
    else:
        # copy values from defaults
        for key in ('address', 'name'):
            if key in args:
                continue
            args[key] = getattr(profile, key)

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

    order = get(order_id, netid, action='edit')
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


def delete(netid, order_id):
    """Deletes the given order.
    Returns True if successful.
    """
    order = get(order_id, netid, action='delete')
    db.session.delete(order)
    db.session.commit()
    return True


def claim(netid, order_id):
    """Assigns the given netid to be the deliverer for the given order.
    Assumes the order is valid to be assigned to someone.
    Returns True if successful.
    """
    deliverer.check(netid)
    order = get(order_id)
    order.delivery_netid = netid
    db.session.commit()
    return True


def unclaim(order_id):
    """Unassigns the deliverer for the given order.
    Returns True if successful.
    """
    order = get(order_id)
    order.delivery_netid = None
    db.session.commit()
    return True


def mark_delivered(order_id):
    """Marks the given order as delivered.
    Returns True if successful.
    """
    order = get(order_id)
    order.is_delivered = True
    order.date_delivered = datetime.utcnow()
    db.session.commit()
    return True
