import flask
from flask import Flask, url_for
from website.views.master import main, page_not_found, access_denied, server_overload, forbidden
import os, sys
from website.content.retrieve import retrieveJson
from website.views.currentstudents import currentstudents
from website.views.committee import committee
from website.views.yourjcr import yourjcr
from website.views.freshers import freshers
from website.views.studentlife import student_routes
from werkzeug.middleware.proxy_fix import ProxyFix


class Request(flask.Request):
    """This specifies locations that the Raven access module will work!"""
    trusted_hosts = {'www.sjcjcr.com', 'sjcjcr.com', 'lpt30.user.srcf.net', 'jfc43.user.srcf.net', 'test.sjcjcr.com', 'localhost', '127.0.0.1', 'ojrb2.user.srcf.net'}

def create_site(config='production'):
    """Create Flask app, specify folder containing static content e.g. imgs, CSS"""
    app = Flask(__name__, instance_relative_config=True, static_folder='assets')

    try:
        app.config.from_object('config.'+config)
    except Exception as e:
        print(e)
        print('Defaulting to production config')
        app.config.from_object('config.production')

    # Load the configuration from the instance folder
    try:
        app.config.from_pyfile('config.py')
    except FileNotFoundError as e:
        print(e)
        print("You need to create the instance/config.py file for secure keys!\n"
            "Make sure the file permissions are chmod 700 if on your own domain.\n"
            "If unsure contact the Computing officer.")
        sys.exit()

    app.request_class = Request
    """Line below ensures app re-directs correctly when running on SRCF server."""
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # IMPORTANT
    """Attach each eaction of the website to the app."""
    app.register_blueprint(main)
    app.register_blueprint(currentstudents)
    app.register_blueprint(freshers)
    app.register_blueprint(yourjcr)
    app.register_blueprint(student_routes)
    app.register_blueprint(committee)
    """Attach error handling functions for relevant error codes."""
    app.register_error_handler(401, access_denied)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_overload)
    return app
