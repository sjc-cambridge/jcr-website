from flask import render_template, request, redirect, Blueprint, url_for
from website.config import auth_decorator

yourjcr= Blueprint('yourjcr', __name__)

@yourjcr.route("/yourjcr/")
def jcr_home():
    return render_template("yourjcr/home.html", a=auth_decorator)

@yourjcr.route('/yourjcr/<pagename>')
def jcr_routing(pagename):
    return render_template("yourjcr/home.html", a=auth_decorator)

@yourjcr.route('/yourjcr/<pagename>/')
def jcr_routing2(pagename):
    return redirect(url_for('/yourjcr/{}'.format(pagename)))
