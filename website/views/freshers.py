from flask import render_template, request, redirect, Blueprint, url_for
from website.helper.auth import johnian_access, JCR

freshers = Blueprint('freshers', __name__)

@freshers.route("/freshers")
@freshers.route("/freshers/home")
def freshers_home():
    crsid=johnian_access.principal
    return render_template("freshers/home.j2.html", JCR=JCR, crsid=crsid, current_page="/freshers")

@freshers.route('/freshers/<pagename>')
def freshers_routing(pagename):
    crsid=johnian_access.principal
    current_page ="/freshers/{}".format(pagename)
    return render_template("freshers/{}.j2.html".format(pagename), JCR=JCR, crsid=crsid, current_page=current_page)


@freshers.route('/freshers/<pagename>/')
def freshers_routing2(pagename):
    return redirect('/freshers/{}'.format(pagename))
