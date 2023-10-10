from flask import render_template

from . import main


@main.app_errorhandler(403)
def forbidden(e):
    """Handle HTTP 403 Forbidden Error."""
    return render_template("403.html"), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """Handle HTTP 404 Page Not Found Error."""
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Handle HTTP 500 Internal Server Error."""
    return render_template("500.html"), 500
