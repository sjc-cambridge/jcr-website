import flask
from flask import Flask, url_for
from website.views.master import main, page_not_found, access_denied, server_overload, forbidden
import os
from website.views.currentstudents import currentstudents
from website.views.yourjcr import yourjcr
from website.views.freshers import freshers
from website.views.studentlife import student_routes
from werkzeug.middleware.proxy_fix import ProxyFix

class Request(flask.Request):
    """This specifies locations that the Raven access module will work!"""
    trusted_hosts = {'jfc43.user.srcf.net', 'localhost'}

def create_site():
    """Create Flask app, specify folder containing static content e.g. imgs, CSS"""
    app = Flask(__name__, static_folder='assets')
    app.request_class = Request
    """Line below doesn't really do anything for us, but required by auth_decorator to work"""
    app.config["SECRET_KEY"] = os.urandom(16)
    """Line below ensures app re-directs correctly when running on SRCF server."""
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # IMPORTANT
    """Attach each eaction of the website to the app."""
    app.register_blueprint(main)
    app.register_blueprint(currentstudents)
    app.register_blueprint(freshers)
    app.register_blueprint(yourjcr)
    app.register_blueprint(student_routes)
    """Attach error handling functions for relevant error codes."""
    app.register_error_handler(401, access_denied)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_overload)
    return app
