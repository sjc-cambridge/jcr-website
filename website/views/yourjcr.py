from flask import render_template, request, redirect, Blueprint, url_for
from website.config import auth_decorator, JCR

yourjcr= Blueprint('yourjcr', __name__)

@yourjcr.route("/yourjcr")
@yourjcr.route("/yourjcr/")
def jcr_home():
    return render_template("yourjcr/home.j2.html", crsid=auth_decorator.principal, current_page ="/yourjcr")

@yourjcr.route('/yourjcr/<pagename>')
def jcr_routing(pagename):
    return render_template("yourjcr/{}.j2.html".format(pagename), crsid=auth_decorator.principal,
                            current_page ="/yourjcr/{}".format(pagename), JCR=JCR)

@yourjcr.route('/yourjcr/<pagename>/')
def jcr_routing2(pagename):
    return redirect(url_for('/yourjcr/{}'.format(pagename)))


@yourjcr.route('/yourjcr/committee/<pagename>')
def jcr_committee_routing(pagename):
    return render_template("yourjcr/committee/{}.j2.html".format(pagename), crsid=auth_decorator.principal,
                            current_page ="/yourjcr/{}".format(pagename), JCR=JCR)

@yourjcr.route('/yourjcr/committee/<pagename>/')
def jcr_committee_routing2(pagename):
    return redirect(url_for('/yourjcr/committee/{}'.format(pagename)))
