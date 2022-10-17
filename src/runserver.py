"""
runserver.py
Runs the server in debug mode.
"""

# ==============================================================================

import sys

from server import app

# ==============================================================================

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as ex:  # pylint: disable=broad-except
        print(ex, file=sys.stderr)
        sys.exit(1)
