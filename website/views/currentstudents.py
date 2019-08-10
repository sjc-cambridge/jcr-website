from flask import Blueprint, render_template
from website.config import auth_decorator

currentstudents = Blueprint('currentstudents', __name__)


@currentstudents.route("/currentstudents")
@currentstudents.route("/currentstudents/")
@currentstudents.route("/currentstudents/home")
@auth_decorator
def current_home():
    user_crsid = auth_decorator.principal
    return render_template("currentstudents/home.html", a=auth_decorator)


@currentstudents.route('/currentstudents/<pagename>')
@auth_decorator
def current_routing(pagename):
    return render_template("/currentstudents/{}.html".format(pagename), a=auth_decorator)


@currentstudents.route('/currentstudents/<pagename>/')
@auth_decorator
def current_routing2(pagename):
    return redirect('/currentstudents/{}'.format(pagename))
