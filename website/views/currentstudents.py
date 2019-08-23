from flask import Blueprint, render_template, send_file, request
import os
from website.config import johnian_access, JCR
from website.contentmanager import get_minutes, get_transparencydoc, get_manifesto, election_json, ELECTIONS_ONGOING


currentstudents = Blueprint('currentstudents', __name__)

@currentstudents.route("/currentstudents")
@currentstudents.route("/currentstudents/")
@currentstudents.route("/currentstudents/home")
@johnian_access
def current_home():
    user_crsid = johnian_access.principal
    return render_template("currentstudents/home.j2.html", crsid=johnian_access.principal, current_page="/currentstudents", JCR=JCR)


@currentstudents.route("/currentstudents/minutes/<filename>")
@johnian_access
def return_minutes(filename):
    try:
        return get_minutes(filename)
    except Exception as e:
        return str(e)


@currentstudents.route("/currentstudents/transparency")
@johnian_access
def return_transparencydoc():
    try:
        return get_transparencydoc()
    except Exception as e:
        return str(e)


@currentstudents.route("/currentstudents/elections")
@johnian_access
def elections_page():
    user_crsid = johnian_access.principal
    if ELECTIONS_ONGOING:  # See contentmanager.py
        template_path="currentstudents/currentelections.j2.html"
    else:
        template_path="currentstudents/electionresults.j2.html"
    return render_template(template_path, crsid=johnian_access.principal, JCR=JCR,
                            current_page="/currentstudents/elections", e=election_json)


@currentstudents.route("/currentstudents/elections/getmanifesto")
@johnian_access
def return_manifesto():
    manifesto = request.args.get('manifesto')
    try:
        return get_manifesto(manifesto)
    except Exception as e:
        return str(e)

@currentstudents.route('/currentstudents/<pagename>')
@johnian_access
def current_routing(pagename):
    return render_template("/currentstudents/{}.j2.html".format(pagename), JCR=JCR,
                            current_page="/currentstudents/{}".format(pagename),
                            crsid=johnian_access.principal)


@currentstudents.route('/currentstudents/<pagename>/')
@johnian_access
def current_routing2(pagename):
    return redirect('/currentstudents/{}'.format(pagename))
