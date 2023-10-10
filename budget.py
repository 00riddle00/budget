#!/usr/bin/env python3

"""Here the Flask application instance is defined."""

import os

from app import create_app, db
from app.models import Expenses, Income, User
from flask_migrate import Migrate

config_name = os.getenv("FLASK_CONFIG") or "default"
app = create_app(config_name)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """Add database object and models to Flask shell context."""
    return dict(
        db=db,
        User=User,
        Income=Income,
        Expenses=Expenses,
    )


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    app.run(debug=True)
