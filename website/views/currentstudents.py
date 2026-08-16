from flask import Blueprint, render_template, send_file, request, redirect, abort
from website.helper.auth import johnian_access, JCR, auth_checker
from website.content.minutes import get_minutes
from website.content.transparency import get_transparency
from website.content.elections import get_manifesto, election_json, ELECTIONS_ONGOING
from website.helper.welfaresystem import userhash


currentstudents = Blueprint("currentstudents", __name__, url_prefix="/currentstudents")


@currentstudents.route("/")
@currentstudents.route("/home")
@johnian_access
def current_home():
    user_crsid = johnian_access.principal
    return render_template(
        "currentstudents/home.j2.html",
        crsid=user_crsid,
        current_page="/currentstudents",
        JCR=JCR,
    )


@currentstudents.route("/elections")
@currentstudents.route("/elections/")
@johnian_access
def elections_page():
    user_crsid = johnian_access.principal
    if ELECTIONS_ONGOING:  # See elections.py
        template_path = "currentstudents/currentelections.j2.html"
    else:
        template_path = "currentstudents/electionresults.j2.html"
    return render_template(
        template_path,
        crsid=user_crsid,
        JCR=JCR,
        current_page="/currentstudents/elections",
        e=election_json,
    )


@currentstudents.route("/elections/getmanifesto")
@johnian_access
def return_manifesto():
    # see elections html pages to understand this.
    manifesto = request.args.get("manifesto")
    try:
        return get_manifesto(manifesto)
    except Exception as e:
        return str(e)


@currentstudents.route("/welfare")
@johnian_access
def welfarepage():
    crsid = johnian_access.principal
    user_code = userhash(crsid)
    return render_template(
        "/currentstudents/welfare.j2.html",
        JCR=JCR,
        current_page="/currentstudents/welfare",
        crsid=crsid,
        user_code=user_code,
    )


@currentstudents.route("/<pagename>")
@johnian_access
def current_routing(pagename):
    try:
        return render_template(
            "/currentstudents/{}.j2.html".format(pagename),
            JCR=JCR,
            current_page="/currentstudents/{}".format(pagename),
            crsid=auth_checker(johnian_access),
        )
    except:
        abort(404)
