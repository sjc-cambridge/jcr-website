from flask import Blueprint, render_template, redirect
from website.helper.auth import johnian_access, JCR
from website.content.studentlife import get_clubs_by_category, get_facilities_by_area

student_routes = Blueprint('studentlife', __name__, url_prefix="/studentlife")


@student_routes.route("/")
@student_routes.route("/home")
def student_home():
    return render_template("studentlife/home.j2.html", JCR=JCR, crsid=johnian_access.principal)


@student_routes.route('/atcambridge')
def student_routing():
    return render_template("studentlife/atcambridge.j2.html", JCR=JCR, crsid=johnian_access.principal)


@student_routes.route("/clubsandsocieties")
def clubsandsocieties():
    clubs_by_category = get_clubs_by_category()
    return render_template("studentlife/clubsandsocieties.j2.html", JCR=JCR, crsid=johnian_access.principal, clubs_by_category=clubs_by_category)


@student_routes.route("/facilities")
def facilities():
    facilities_by_area = get_facilities_by_area()
    return render_template("studentlife/facilities.j2.html", JCR=JCR, crsid=johnian_access.principal, facilities_by_area=facilities_by_area)
