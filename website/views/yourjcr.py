from flask import render_template, request, redirect, Blueprint, url_for, flash, get_flashed_messages
from website.helper.auth import johnian_access, JCR, is_human, captchapublickey
from website.content.minutes import get_minutes_dict, get_minutes
from website.content.documents import send_constitution
import datetime

yourjcr = Blueprint("yourjcr", __name__)


@yourjcr.route("/yourjcr")
@yourjcr.route("/yourjcr/home")
def jcr_home():
    return render_template("yourjcr/home.j2.html", JCR=JCR, crsid=johnian_access.principal, current_page="/yourjcr")


@yourjcr.route("/yourjcr/minutes")
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

    sitekey = "6LdI-LgUAAAAAM7BWzlvLCKuFR5p0jFTqaOpoo-L"

    if request.method == 'POST':
        recipient = request.form['recipient']
        senderName = request.form['senderName']
        senderEmail = request.form['senderEmail']
        subject = request.form['subject']
        message = request.form['message']
        captcha_response = request.form['g-recaptcha-response']

        if not is_human(captcha_response):
            # Process request here
            flash("Please verify you're a human!")
            return redirect(url_for("yourjcr.contact"))

        flash("Your message has been sent! If you would like to send another message, fill in the form again below.")

        wrapped_message = "Hi {}!\n\nYou have been contacted by {} via the JCR website. Their message is as " \
                          "follows:\n\n\"{}\"\n\nIf you would like to reply, their email is {}.\n\nSouvent " \
                          "Me Souvient".format(JCR[recipient]['name'], senderName, message, senderEmail)
        JCR.email_member(subject, wrapped_message, recipient)

        return redirect(url_for("yourjcr.contact"))
    else:
        return render_template("yourjcr/contact.j2.html", crsid=johnian_access.principal,
                               current_page="/yourjcr/contact", JCR=JCR, sitekey=captchapublickey)


@yourjcr.route("/yourjcr/constitution")
@johnian_access
def return_constitution():
    return send_constitution()


@yourjcr.route("/yourjcr/<pagename>")
def jcr_routing(pagename):
    return render_template("yourjcr/{}.j2.html".format(pagename), crsid=johnian_access.principal,
                           current_page="/yourjcr/{}".format(pagename), JCR=JCR)


@yourjcr.route("/yourjcr/<pagename>/")
def jcr_routing2(pagename):
    return redirect(url_for("/yourjcr/{}".format(pagename)))


@yourjcr.route("/yourjcr/committee/<pagename>")
def jcr_committee_routing(pagename):
    if pagename == 'fwelfare':
        member = JCR['welfare']['fnb']
    elif pagename == 'mwelfare':
        member = JCR['welfare']['mnb']
    else:
        member = JCR[pagename]

    if pagename == 'president':
        role = JCR['president']['role']
        name = "{} & {}".format(JCR['president']['co1']['name'],JCR['president']['co2']['name'])
        member_crsid = "{} & {}".format(JCR['president']['co1']['crsid'], JCR['president']['co2']['crsid'])
        bio = JCR['president']['bio']
        img = JCR['president']['img']
    else:
        role = member['role']
        name = member['name']
        member_crsid = member['crsid']
        bio = member['bio']
        img = member['img']
    return render_template("yourjcr/committee/committeeprofile.j2.html", crsid=johnian_access.principal, role=role, name=name, member_crsid=member_crsid, bio=bio, img=img,
                           current_page="/yourjcr/{}".format(pagename), JCR=JCR)


@yourjcr.route("/yourjcr/committee/<pagename>/")
def jcr_committee_routing2(pagename):
    return redirect(url_for("/yourjcr/committee/{}".format(pagename)))
