import ucam_webauth
import ucam_webauth.raven
import ucam_webauth.raven.flask_glue
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pickle
import smtplib
import json

"""
    This file creates the JCR object which is used for committee verification,
    sending emails and displaying members in the YourJCR section.
    To change a JCR member e.g. at handover simply edit their name, crsid and bio
    in content/committee.json and make sure the new JCR officers image replaces
    theirs with the same (role) name in assets/img/committee e.g. Computing.jpg

    This should change all instances of the officer's name on the website to the
    new officer since we have used jinja syntax e.g. JCR['position']['name'].
    Although if the name of a role changes (e.g. co-presidents to president)
    you will need to edit /yourjcr/committee.j2.html and the relevant officer page.

    The file also creates johnian_access and committee_access, which are
    decorator classes which restrict pages appropriately.
"""

script_dir = os.path.dirname(__file__)

with open(os.path.join(script_dir, "johnians.txt"), "rb") as file:
    johnian_crsids = set(pickle.load(file))


#johnian_crsids.remove('jfc43') #Testing login works by removing myself

"""This decorator restricts pages to Johnians."""
johnian_access = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 6000,
                                            require_principal = johnian_crsids)

class Committee(dict):
    """Committee object is a sub-class of dictionary (for neat indexing)
        also has email methods useful for contact us and committee pages."""
    '''To do: edit .forward function.
        Send PDF minutes, do committee page'''
    def __init__(self, committee_json_path, *args):
        dict.__init__(self, *args)
        self.path = os.path.join(script_dir, committee_json_path)
        self.committee_crsids = []
        with open(self.path, 'r') as f:
            committee_json = json.load(f)
            for key, item in committee_json.items():
                self[key] = item
                for key2, item2 in item.items():
                    if key2 == 'crsid':
                        self.committee_crsids.append(item2)
                    else: # Sub-dict, e.g. welfare officers
                        if isinstance(item2, dict):
                            self.committee_crsids.append(item2['crsid'])

        self.committee_crsids = set(self.committee_crsids)

    def email_member(self, subject, input_message, committee_role):
        """Email committee member"""
        self.email_people(subject, input_message, [committee_role + '@sjcjcr.com'])
        return "Emailed {}".format(self[committee_role]['name'])

    def email_committee(self, subject, input_message):
        """Email entire committee"""
        committee_emails = [role + '@sjcjcr.com' for role in self.keys()]
        self.email_people(subject, input_message, committee_emails)
        return "Emailed JCR Committee"

    def email_someone(self, subject, input_message, email_address):
        """Email committee member"""
        self.email_people(subject, input_message, [email_address])
        return "Emailed {}".format(email_address)

    def email_people(self, subject, input_message, address_list, reply_to = None, attachment=None):
        """Email a list of emails Gmail account uses 2-factor authentication so
            password used won't work anywhere else."""

        recipients_string = ", ".join(address_list)
        message = MIMEMultipart()
        gmail_user = 'sjcjcrmisc@gmail.com'
        message["From"] = gmail_user
        message["To"] = recipients_string
        message["Subject"] = subject
        if reply_to:
            message["reply-to"] = reply_to

        message.attach(MIMEText(input_message, "plain"))

        if attachment:
            # Open PDF file in binary mode
            with open(os.path.join(script_dir, attachment), "rb") as file:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                "attachment; filename= {}".format(attachment),
            )

            # Add attachment to message and convert message to string
            message.attach(part)

        with open(os.path.join(script_dir, "config.txt"), "r") as file:
            app_key = file.readlines()[0] # See https://support.google.com/accounts/answer/185833?hl=en
        gmail_pwd = app_key # App password not re-usable see above.
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(gmail_user, gmail_pwd)
        smtpserver.sendmail(gmail_user, address_list, message.as_string())
        smtpserver.close()
        return "Email sent!"

JCR = Committee("content/committee.json")

# Committee access decorator for restricting committee section of website.
committee_access = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 6000, require_principal = JCR.committee_crsids)
#print(JCR['PRESIDENT']['name'])
#print(JCR['COMPUTING']['name'])

#print(JCR.email_member("St. John's Emailer", "Here are last weeks minutes",'computing')) # Pls don't spam meh
