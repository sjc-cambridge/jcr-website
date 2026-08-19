from flask import render_template, request, redirect, Blueprint, url_for, abort
from website.helper.auth import johnian_access, JCR, auth_checker
from website.content.documents import send_fresherguide

freshers = Blueprint("freshers", __name__)


@freshers.route("/freshers/")
@freshers.route("/freshers/home")
def freshers_home():
    crsid = auth_checker(johnian_access)
    return render_template(
        "freshers/home.j2.html", JCR=JCR, crsid=crsid, current_page="/freshers"
    )


@freshers.route("/freshers/guide")
def return_guide():
    return send_fresherguide()


@freshers.route("/freshers/<pagename>")
def freshers_routing(pagename):
    crsid = auth_checker(johnian_access)
    current_page = "/freshers/{}".format(pagename)
    try:
        return render_template(
            "freshers/{}.j2.html".format(pagename),
            JCR=JCR,
            crsid=crsid,
            current_page=current_page,
        )
    except:
        abort(404)
