from flask import Blueprint, render_template, redirect, url_for
from website.config import auth_decorator

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html", a=auth_decorator)

@main.route("/login/")
def login():
    return redirect(url_for("main.home"))

@main.route("/logout/")
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
