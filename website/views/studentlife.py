from flask import Blueprint, render_template
from website.config import auth_decorator
from website.content.retrieve import retrieveJson

student_routes = Blueprint('studentlife', __name__)

@student_routes.route("/studentlife")
@student_routes.route("/studentlife/")
def student_home():
    return render_template("studentlife/home.html", a=auth_decorator)

@student_routes.route('/studentlife/<pagename>')
def student_routing(pagename):
    return render_template("freshers/{}.html".format(pagename), a=auth_decorator)


@student_routes.route('/studentlife/<pagename>/')
def student_routing2(pagename):
    return redirect('/studentlife/{}'.format(pagename))
