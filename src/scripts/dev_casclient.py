"""
dev_casclient.py
A CasClient implementation for development.
"""

# ==============================================================================

from flask import abort, redirect, session

# ==============================================================================


class DevCasClient:
    """A CasClient implementation for development."""

    def __init__(self, username):
        self.username = username

    def authenticate(self):
        session['username'] = self.username

    def logout(self, logout_url):
        session.pop('username')

        abort(redirect(logout_url))
