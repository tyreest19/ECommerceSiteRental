from app.error import error
from flask import render_template


@error.app_errorhandler(404)
@error.app_errorhandler(403)
@error.app_errorhandler(410)
def page_not_found(e):
    return render_template('404.html'), 404

@error.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500