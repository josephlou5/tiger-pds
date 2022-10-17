"""
server.py
Hosts the server for the app.
"""

# ==============================================================================

import functools

from flask import (Flask, make_response, redirect, render_template, request,
                   session, url_for)

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


def login_required(func):
    """A decorator to protect an endpoint."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session['current_page'] = request.path
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


# ==============================================================================


@app.route('/', methods=['GET'])
def index():
    return _render('index.jinja')


# ==============================================================================


@app.route('/orders', methods=['GET'])
@login_required
def orders():
    return _render('orders/orders.jinja')


@app.route('/orders/new', methods=['GET'])
@login_required
def create_order():
    return _render('orders/create_order_form.jinja')


# ==============================================================================


@app.route('/history', methods=['GET'])
@login_required
def history():
    return _render('history/history.jinja')


# ==============================================================================


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return _render('profile/profile.jinja')


# ==============================================================================

if __name__ == '__main__':
    app.run('localhost', debug=True)
