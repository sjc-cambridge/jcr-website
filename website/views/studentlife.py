from flask import Blueprint, render_template
from website.config import auth_decorator
from website.content.retrieve import retrieveJson

student_routes = Blueprint('studentlife', __name__)

@student_routes.route("/studentlife")
@student_routes.route("/studentlife/")
def student_home():
    return render_template("studentlife/home.j2.html", a=auth_decorator, current_page ="/studentlife")

@student_routes.route('/studentlife/<pagename>')
def student_routing(pagename):
    return render_template("studentlife/{}.j2.html".format(pagename), a=auth_decorator, current_page ="/studentlife/{}".format(pagename))


@student_routes.route('/studentlife/<pagename>/')
def student_routing2(pagename):
    return redirect('/studentlife/{}'.format(pagename))
