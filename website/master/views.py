from flask import render_template, request, redirect, Blueprint, url_for
from website.config import auth_decorator
from website.welfaresystem import userhash

main = Blueprint('main', __name__,template_folder='templates',static_folder='templates/assets')

@main.route("/yourjcr/")
def jcr_home():
    return render_template("yourjcr/home.html", a=auth_decorator)

@main.route('/yourjcr/<pagename>')
def jcr_routing(pagename):
    return render_template("yourjcr/home.html", a=auth_decorator)

@main.route('/yourjcr/<pagename>/')
def jcr_routing2(pagename):
    return redirect('/yourjcr/{}'.format(pagename))


# @main.route("/studentlife")
# def student_home():
#     return render_template("studentlife/home.html", a=auth_decorator)

# @main.route('/studentlife/<pagename>')
# def student_routing(pagename):
#     if pagename == 'home':
#         return render_template("studentlife/home.html", a=auth_decorator)
#     try:
#         return render_template("studentlife/{}.html".format(pagename), a=auth_decorator)
#     except:
#         error(404)


@main.route("/freshers")
@main.route("/freshers/home")
def freshers_home():
    return render_template("freshers/home.html", a=auth_decorator)

@main.route('/freshers/<pagename>')
def freshers_routing(pagename):
    return render_template("freshers/{}.html".format(pagename), a=auth_decorator)


@main.route('/freshers/<pagename>/')
def freshers_routing2(pagename):
    return redirect('/freshers/{}'.format(pagename))


@auth_decorator
@main.route("/currentstudents")
@main.route("/currentstudents/home")
@auth_decorator
def current_home():
    user_crsid = auth_decorator.principal
    return render_template("currentstudents/home.html", a=auth_decorator)

@auth_decorator
@main.route('/currentstudents/<pagename>')
def current_routing(pagename):
    return render_template("currentstudents/{}.html".format(pagename), a=auth_decorator)

@auth_decorator
@main.route('/currentstudents/<pagename>/')
def current_routing2(pagename):
    return redirect('/currentstudents/{}'.format(pagename))

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html", a=auth_decorator)

@main.route("/login/")
@auth_decorator
def login():
    return redirect(url_for("main.home"))

@main.route("/logout/")
@auth_decorator
def logout():
    auth_decorator.logout()
    return redirect(url_for("main.home"))

def access_denied(e):
    return redirect(url_for("main.error401"))

def forbidden(e):
    return redirect(url_for("main.error403"))

def page_not_found(e):
    return redirect(url_for("main.error404"))

def server_overload(e):
    return redirect(url_for("main.error500"))

@main.route("/401")
def error401():
    return render_template('401.html')

@main.route("/403")
def error403():
    return render_template('403.html')

@main.route("/404")
def error404():
    return render_template('404.html')

@main.route("/500")
def error500():
    return render_template('500.html')
