from flask import render_template, request, redirect, Blueprint, url_for
from website.config import johnian_access, JCR
from website.contentmanager import get_minutes_dict, get_minutes
from website.forms import ContactForm
import datetime

yourjcr = Blueprint('yourjcr', __name__)


@yourjcr.route("/yourjcr")
@yourjcr.route("/yourjcr/")
def jcr_home():
    return render_template("yourjcr/home.j2.html", JCR=JCR, crsid=johnian_access.principal, current_page="/yourjcr")


@yourjcr.route('/yourjcr/minutes')
@johnian_access
def minutes_page():
    if request.args:
        academicyear = request.args.get("academicyear")  # e.g. 2019/2020
        term = request.args.get("term")
        filename = request.args.get("filename")
        try:
            return get_minutes(term, academicyear, filename)
        except Exception as e:
            print(e)
            return str(e)
    minutes_dict = get_minutes_dict()
    return render_template("yourjcr/minutes.j2.html", crsid=johnian_access.principal,
                           current_page="/yourjcr/minutes", JCR=JCR, minutes_dict=minutes_dict,
                           sorted=sorted)

@yourjcr.route('/yourjcr/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        return 'Form posted'
    elif request.method == 'GET':
        return render_template("yourjcr/contact.j2.html", crsid=johnian_access.principal,
                               current_page="/yourjcr/current", JCR=JCR, form=form)

@yourjcr.route('/yourjcr/<pagename>')
def jcr_routing(pagename):
    return render_template("yourjcr/{}.j2.html".format(pagename), crsid=johnian_access.principal,
                            current_page="/yourjcr/{}".format(pagename), JCR=JCR)


@yourjcr.route('/yourjcr/<pagename>/')
def jcr_routing2(pagename):
    return redirect(url_for('/yourjcr/{}'.format(pagename)))


@yourjcr.route('/yourjcr/committee/<pagename>')
def jcr_committee_routing(pagename):
    return render_template("yourjcr/committee/{}.j2.html".format(pagename), crsid=johnian_access.principal,
                           current_page="/yourjcr/{}".format(pagename), JCR=JCR)


@yourjcr.route('/yourjcr/committee/<pagename>/')
def jcr_committee_routing2(pagename):
    return redirect(url_for('/yourjcr/committee/{}'.format(pagename)))
