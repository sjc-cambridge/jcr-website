from flask import Blueprint, render_template, redirect, url_for, request, current_app
from website.helper.auth import johnian_access, JCR, auth_checker
from website.content.documents import send_helpdoc

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.j2.html", crsid=auth_checker(johnian_access), JCR=JCR, current_page="/")

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

@main.route("/gettinghelp")
def getting_help():
    return send_helpdoc()

def access_denied(e):
    return render_template('401.j2.html', crsid=auth_checker(johnian_access), JCR=JCR), 401

def forbidden(e):
    return render_template('403.j2.html', crsid=auth_checker(johnian_access), JCR=JCR), 403

def page_not_found(e):
    return render_template('404.j2.html', crsid=auth_checker(johnian_access), JCR=JCR), 404

def server_overload(e):
    """Inform computing officer of server error"""
    app_pwd = current_app.config["GMAIL_KEY"]
    error_msg = "Server error encountered by a user accessing {}".format(request.url)
    JCR.email_member('Error 500', error_msg, 'computing', app_pwd)
    return render_template('500.j2.html', crsid=auth_checker(johnian_access), JCR=JCR), 500
