import flask
from flask import Flask, url_for
from website.views.master import main, page_not_found, access_denied, server_overload, forbidden
import os
from website.views.currentstudents import currentstudents
from website.views.yourjcr import yourjcr
from website.views.freshers import freshers
from website.views.studentlife import student_routes

class Request(flask.Request):
    trusted_hosts = {'jfc43.user.srcf.net', 'localhost'}

from werkzeug.middleware.proxy_fix import ProxyFix

def create_site():
    app = Flask(__name__, static_folder='templates/assets')
    app.request_class = Request
    app.config["SECRET_KEY"] = os.urandom(16)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.register_blueprint(main)
    app.register_blueprint(currentstudents)
    app.register_blueprint(freshers)
    app.register_blueprint(yourjcr)
    app.register_blueprint(student_routes)
    app.register_error_handler(401, access_denied)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_overload)
    return app
