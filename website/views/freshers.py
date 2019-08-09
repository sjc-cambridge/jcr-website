from flask import render_template, request, redirect, Blueprint, url_for
from website.config import auth_decorator

freshers = Blueprint('freshers', __name__)

@freshers.route("/freshers")
@freshers.route("/freshers/home")
def freshers_home():
    return render_template("freshers/home.html", a=auth_decorator)

@freshers.route('/freshers/<pagename>')
def freshers_routing(pagename):
    return render_template("freshers/{}.html".format(pagename), a=auth_decorator)


@freshers.route('/freshers/<pagename>/')
def freshers_routing2(pagename):
    return redirect('/freshers/{}'.format(pagename))
