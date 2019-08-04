import flask
from flask import Flask, url_for
from website.master.views import main, page_not_found, access_denied, server_overload, forbidden
import os

from website.views.studentlife import student_routes

class Request(flask.Request):
    trusted_hosts = {'localhost', '0.0.0.0', '127.0.0.1', 'ojrb2.user.srcf.net', 'test.sjcjcr.com',
                        'jfc43.user.srcf.net',}

def create_site():
    app = Flask(__name__)
    app.request_class = Request
    app.config["SECRET_KEY"] = os.urandom(16)
    app.register_blueprint(main)
    app.register_error_handler(401, access_denied)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_overload)
    app.register_blueprint(student_routes)
    return app
