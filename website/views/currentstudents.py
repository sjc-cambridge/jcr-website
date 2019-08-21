from flask import Blueprint, render_template, send_file
import os
from website.config import auth_decorator
from website.contentmanager import get_minutes, get_transparencydoc

currentstudents = Blueprint('currentstudents', __name__)

@currentstudents.route("/currentstudents")
@currentstudents.route("/currentstudents/")
@currentstudents.route("/currentstudents/home")
@auth_decorator
def current_home():
    user_crsid = auth_decorator.principal
    return render_template("currentstudents/home.j2.html", crsid=auth_decorator.principal, current_page="/currentstudents")

@auth_decorator
@currentstudents.route("/currentstudents/minutes/<filename>")
def return_minutes(filename):
    try:
        return get_minutes(filename)
    except Exception as e:
        return str(e)

@auth_decorator
@currentstudents.route("/currentstudents/transparency")
def return_transparencydoc():
    try:
        return get_transparencydoc()
    except Exception as e:
        return str(e)

@currentstudents.route('/currentstudents/<pagename>')
@auth_decorator
def current_routing(pagename):
    return render_template("/currentstudents/{}.j2.html".format(pagename), crsid=auth_decorator.principal, current_page="/currentstudents/{}".format(pagename))


@currentstudents.route('/currentstudents/<pagename>/')
@auth_decorator
def current_routing2(pagename):
    return redirect('/currentstudents/{}'.format(pagename))
