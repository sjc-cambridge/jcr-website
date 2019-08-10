from flask import Blueprint, render_template, redirect, url_for
from website.config import auth_decorator

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@auth_decorator
def home():
    print(url_for("main.error500"))
    print('Getting here')
    print(url_for("main.error500", _external=True))
    return render_template("index.html", a=auth_decorator)

@main.route("/login")
def login_route():
    print('LOGIN')
    print(url_for("main.home", _external=True))
    return render_template("index.html", a=auth_decorator)
    #return redirect(url_for("main.home", _external=True))

@main.route("/logout")
def logout_route():
    auth_decorator.logout()
    print(url_for("main.home",_external=True))
    return redirect(url_for("main.home", _external=True))

def access_denied(e):
    print(url_for("main.error401", _external=True))
    return redirect(url_for("main.error401", _external=True))

def forbidden(e):
    print(url_for("main.error403", _external=True))
    return redirect(url_for("main.error403", _external=True))

def page_not_found(e):
    print(url_for("main.error404", _external=True))
    return redirect(url_for("main.error404", _external=True))

def server_overload(e):
    print(url_for("main.error500", _external=True))
    return redirect(url_for("main.error500", _external=True))

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
