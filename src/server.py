"""
server.py
Hosts the server for the app.
"""

# ==============================================================================

import functools

from flask import (Flask, make_response, redirect, render_template, request,
                   session, url_for)
from flask_wtf.csrf import CSRFProtect

import db
import forms
from config import get_config
from scripts.casclient import CasClient, DevCasClient

# ==============================================================================

# Set up app

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(get_config(app.debug))

if app.debug:
    cas_client = DevCasClient('jdlou')
else:
    cas_client = CasClient()

# Set up CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)

# Set up database
db.init_app(app)

# ==============================================================================


def get_netid():
    return session.get('username')


def is_logged_in():
    return get_netid() is not None


@app.context_processor
def inject_logged_in_user():
    return {
        'is_logged_in': is_logged_in(),
        'netid': get_netid(),
    }


# ==============================================================================


def set_current_page():
    session['current_page'] = request.path


def login_required(func):
    """A decorator to protect an endpoint."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        set_current_page()
        if not is_logged_in():
            return redirect(url_for('log_in'))
        return func(*args, **kwargs)

    return wrapper


# ==============================================================================


def _get_redirect_url():
    redirect_url = session.get('current_page')
    if redirect_url is None:
        return url_for('index')
    return redirect_url


@app.route('/log_in', methods=['GET'])
def log_in():
    cas_client.authenticate()
    return redirect(_get_redirect_url())


@app.route('/log_out', methods=['GET'])
def log_out():
    cas_client.authenticate()
    # After logging out, always redirect to index
    cas_client.logout(url_for('index'))


# ==============================================================================


def _render(template_file, **kwargs):
    html = render_template(template_file, **kwargs)
    response = make_response(html)
    return response


def error_view(title, message):
    return _render('error.jinja', title=title, message=message)


def unauthorized_access():
    return error_view('Unauthorized access',
                      'You do not have permission to view this page.')


# ==============================================================================


@app.route('/', methods=['GET'])
def index():
    set_current_page()
    return _render('index.jinja')


# ==============================================================================


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    netid = get_netid()
    user_profile = db.user_profile.get(netid)

    edit_profile_form = forms.EditProfileForm(obj=user_profile)

    if edit_profile_form.validate_on_submit():
        db.user_profile.save(netid, edit_profile_form)

    render_kwargs = {
        'form': edit_profile_form,
        'endpoint': url_for('profile'),
    }
    return _render('profile/profile.jinja', **render_kwargs)


# ==============================================================================


@app.route('/orders', methods=['GET'])
@login_required
def orders():
    all_orders = db.order.get_all(get_netid())
    return _render('orders/orders.jinja', orders=all_orders)


def _get_order(order_id):
    order = db.order.get(order_id)
    if order is None:
        return None, lambda: error_view('Unknown order',
                                        'This order does not exist.')
    if order.netid != get_netid():
        return None, unauthorized_access
    return order, None


@app.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def view_order(order_id):
    order, error = _get_order(order_id)
    if error is not None:
        return error()
    return _render('orders/order_info.jinja', order=order)


@app.route('/orders/new', methods=['GET', 'POST'])
@login_required
def create_order():
    netid = get_netid()

    user_profile = db.user_profile.get(netid)
    create_order_form = forms.EditOrderForm(obj=None)
    del create_order_form.delete

    if create_order_form.validate_on_submit():
        success = db.order.create(netid, user_profile, create_order_form)
        if success:
            return redirect(url_for('orders'))

    profile_placeholders = {}
    if user_profile is None:
        for key in ('address', 'name'):
            profile_placeholders[key] = ''
    else:
        for key in ('address', 'name'):
            profile_placeholders[key] = getattr(user_profile, key, '')

    render_kwargs = {
        'creating': True,
        'form': create_order_form,
        'endpoint': url_for('create_order'),
        'cancel_link': url_for('orders'),
        'profile': profile_placeholders,
    }
    return _render('orders/edit_order_form.jinja', **render_kwargs)


@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order, error = _get_order(order_id)
    if error is not None:
        return error()

    edit_order_form = forms.EditOrderForm(obj=order)

    if edit_order_form.data['delete']:
        success = db.order.delete(order_id)
        if success:
            return redirect(url_for('orders'))

    if edit_order_form.validate_on_submit():
        success = db.order.update(get_netid(), order_id, edit_order_form)
        if success:
            return redirect(url_for('orders'))

    render_kwargs = {
        'creating': False,
        'form': edit_order_form,
        'endpoint': url_for('edit_order', order_id=order_id),
        'cancel_link': url_for('orders'),
        'profile': {key: '' for key in ('address', 'name')},
    }
    return _render('orders/edit_order_form.jinja', **render_kwargs)


# ==============================================================================


@app.route('/history', methods=['GET'])
@login_required
def history():
    return _render('history/history.jinja')
