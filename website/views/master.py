from flask import Blueprint, render_template, redirect, url_for, request
from website.helper.auth import johnian_access, JCR

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.j2.html", crsid=johnian_access.principal, JCR=JCR, current_page="/")

@main.route("/login")
@johnian_access
def login_route():
    return_url = request.args.get('redirect')
    if return_url:
        return redirect(return_url)
    else:
        return redirect(url_for("main.home"))

@main.route("/logout")
def logout_route():
    johnian_access.logout()
    return_url = request.args.get('redirect')
    if return_url:
        if 'committee' not in return_url and 'currentstudents' not in return_url:
            return redirect(return_url)
        else:
            return redirect(url_for("main.home"))
    else:
        return redirect(url_for("main.home"))

def access_denied(e):
    return render_template('401.j2.html', crsid=johnian_access.principal, JCR=JCR)

def forbidden(e):
    return render_template('403.j2.html', crsid=johnian_access.principal, JCR=JCR)

def page_not_found(e):
    return render_template('404.j2.html', crsid=johnian_access.principal, JCR=JCR)

def server_overload(e):
    return render_template('500.j2.html', crsid=johnian_access.principal, JCR=JCR)
