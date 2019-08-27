from flask import Blueprint, render_template, redirect
from website.config import johnian_access, JCR
from website.content.retrieve import retrieveJson

student_routes = Blueprint('studentlife', __name__)


@student_routes.route("/studentlife")
@student_routes.route("/studentlife/")
def student_home():
    return render_template("studentlife/home.j2.html", JCR=JCR, crsid=johnian_access.principal, current_page="/studentlife")


@student_routes.route('/studentlife/atcambridge')
def student_routing(pagename):
    return render_template("studentlife/atcambridge.j2.html".format(pagename), JCR=JCR, crsid=johnian_access.principal, current_page="/studentlife/{}".format(pagename))


@student_routes.route("/studentlife/clubsandsocieties")
def clubsandsocieties():
    clubs_by_category = retrieveJson("studentlife/clubsandsocieties")
    return render_template("studentlife/clubsandsocieties.j2.html", JCR=JCR, crsid=johnian_access.principal, clubs_by_category=clubs_by_category)


@student_routes.route("/studentlife/facilities")
def facilities():
    facilities_by_area = retrieveJson("studentlife/facilities")
    return render_template("studentlife/facilities.j2.html", JCR=JCR, crsid=johnian_access.principal, facilities_by_area=facilities_by_area)
