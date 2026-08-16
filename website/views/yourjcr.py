from flask import (
    render_template,
    request,
    redirect,
    Blueprint,
    url_for,
    flash,
    get_flashed_messages,
    current_app,
    abort,
)
from website.helper.auth import (
    johnian_access,
    JCR,
    is_human,
    captchapublickey,
    auth_checker,
)
from website.content.minutes import get_minutes_dict, get_minutes
from website.content.transparency import get_transparency_dict, get_transparency
from website.content.documents import (
    send_constitution,
    send_financialaid,
    send_financialaid_spreadsheet,
)
import datetime

yourjcr = Blueprint("yourjcr", __name__, url_prefix="/yourjcr")


@yourjcr.route("/")
@yourjcr.route("/home")
def jcr_home():
    return render_template(
        "yourjcr/home.j2.html",
        JCR=JCR,
        crsid=auth_checker(johnian_access),
        current_page="/yourjcr",
    )


@yourjcr.route("/minutes")
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
    return render_template(
        "yourjcr/minutes.j2.html",
        crsid=auth_checker(johnian_access),
        current_page="/yourjcr/minutes",
        JCR=JCR,
        minutes_dict=minutes_dict,
        sorted=sorted,
    )


@yourjcr.route("/transparency")
@johnian_access
def transparency_page():
    if request.args:
        academicyear = request.args.get("academicyear")  # e.g. 2019/2020
        term = request.args.get("term")
        filename = request.args.get("filename")
        try:
            return get_transparency(term, academicyear, filename)
        except Exception as e:
            print(e)
            return str(e)
    transparency_dict = get_transparency_dict()
    return render_template(
        "yourjcr/transparency.j2.html",
        crsid=auth_checker(johnian_access),
        current_page="/yourjcr/transparency",
        JCR=JCR,
        transparency_dict=transparency_dict,
        sorted=sorted,
    )


@yourjcr.route("/contact", methods=["GET", "POST"])
def contact():
    sitekey = current_app.config["CAPTCHA_PUBLIC"]
    privatekey = current_app.config["CAPTCHA_PRIVATE"]
    app_pwd = current_app.config["GMAIL_KEY"]

    role_str = request.args.get("role")

    if request.method == "POST":
        recipient = request.form["recipient"]
        senderName = request.form["senderName"]
        senderEmail = request.form["senderEmail"]
        subject = request.form["subject"]
        message = request.form["message"]
        captcha_response = request.form["g-recaptcha-response"]
        if not is_human(captcha_response, privatekey):
            # Process request here
            flash("Please verify you're a human!")
            return redirect(url_for("yourjcr.contact"))

        flash(
            "Your message has been sent! If you would like to send another message, fill in the form again below."
        )

        if recipient in ["mnb", "fnb"]:
            recipientName = JCR["welfare"][recipient]["name"]
            recipient = "welfare"
        else:
            recipientName = JCR[recipient]["name"]
        wrapped_message = (
            "Hi {}!\n\nYou have been contacted by {} via the JCR website. Their message is as "
            'follows:\n\n"{}"\n\nIf you would like to reply, their email is {}.\n\nSouvent '
            "Me Souvient\n\n Note: This inbox is not tracked so don't reply to it! Message "
            "the computing officer if you have any queries!".format(
                recipientName, senderName, message, senderEmail
            )
        )

        JCR.email_member(subject, wrapped_message, recipient, app_pwd)

        return redirect(url_for("yourjcr.contact"))
    else:
        return render_template(
            "yourjcr/contact.j2.html",
            crsid=auth_checker(johnian_access),
            role_str=role_str,
            current_page="/yourjcr/contact",
            JCR=JCR,
            sitekey=sitekey,
        )


@yourjcr.route("/constitution")
@johnian_access
def return_constitution():
    return send_constitution()


@yourjcr.route("/financialaid")
def return_financialaid():
    return send_financialaid()


# @yourjcr.route("/financialaid-spreadsheet")
# def return_financialaid_spreadsheet():
#     return send_financialaid_spreadsheet()


@yourjcr.route("/<pagename>")
def jcr_routing(pagename):
    try:
        return render_template(
            "yourjcr/{}.j2.html".format(pagename),
            crsid=auth_checker(johnian_access),
            current_page="/yourjcr/{}".format(pagename),
            JCR=JCR,
        )
    except:
        abort(404)


@yourjcr.route("/committee/<pagename>")
def jcr_committee_routing(pagename):
    if pagename == "fwelfare":
        member = JCR["welfare"]["fnb"]
        role_str = "fnb"
        email = "welfare"
    elif pagename == "mwelfare":
        member = JCR["welfare"]["mnb"]
        role_str = "mnb"
        email = "welfare"
    elif pagename in JCR:
        member = JCR[pagename]
        role_str = pagename
        email = pagename
    else:
        abort(404)

    email += "@sjcjcr.com"

    if pagename == "president":
        role = JCR["president"]["role"]
        name = "{} & {}".format(
            JCR["president"]["co1"]["name"], JCR["president"]["co2"]["name"]
        )
        member_crsid = "{} & {}".format(
            JCR["president"]["co1"]["crsid"], JCR["president"]["co2"]["crsid"]
        )
        bio = JCR["president"]["bio"]
        img = JCR["president"]["img"]
    else:
        role = member["role"]
        name = member["name"]
        member_crsid = member["crsid"]
        bio = member["bio"]
        img = member["img"]

    return render_template(
        "yourjcr/committee/committeeprofile.j2.html",
        crsid=auth_checker(johnian_access),
        role_str=role_str,
        email=email,
        name=name,
        member_crsid=member_crsid,
        bio=bio,
        img=img,
        current_page="/yourjcr/{}".format(pagename),
        JCR=JCR,
    )
