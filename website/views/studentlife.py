from flask import Blueprint, render_template
from website.config import auth_decorator
from website.content.retrieve import retrieveJson

student_routes = Blueprint('studentlife', __name__)


@student_routes.route("/studentlife")
def index():
    return render_template("studentlife/index.j2.html", a=auth_decorator)


@student_routes.route("/studentlife/glossary")
def glossary():
    glossary_items = retrieveJson("studentlife/glossary")
    return render_template("studentlife/glossary.j2.html", a=auth_decorator, glossary_items=glossary_items)


@student_routes.route("/studentlife/facilities")
def facilities():
    facilities_by_area = retrieveJson("studentlife/facilities")
    return render_template("studentlife/facilities.j2.html", a=auth_decorator, facilities_by_area=facilities_by_area)


@student_routes.route("/studentlife/clubsandsocieties")
def clubsandsocieties():
    clubs_by_category = retrieveJson("studentlife/clubsandsocieties")
    return render_template("studentlife/clubsandsocieties.j2.html", a=auth_decorator, clubs_by_category=clubs_by_category)
