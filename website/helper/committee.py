from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from website.content.retrieve import retrieveBinary
from website.content.committee import get_committee_json

script_dir = os.path.dirname(__file__)


class Committee(dict):
    """Committee object is a sub-class of dictionary (for neat indexing)
        also has email methods useful for contact us and committee pages."""

    """ TODO:
    - edit .forward function.
    - Send PDF minutes
    """

    def __init__(self):
        dict.__init__(self)
        self.committee_crsids = []
        #self.app_pwd = app_pwd

        committee_json = get_committee_json()

        for key, item in committee_json.items():
            self[key] = item
            for key2, item2 in item.items():
                if key2 == 'crsid':
                    self.committee_crsids.append(item2)
                else:  # Sub-dict, e.g. welfare officers
                    if isinstance(item2, dict):
                        self.committee_crsids.append(item2['crsid'])

        self.committee_crsids = set(self.committee_crsids)

    def email_member(self, subject, input_message, committee_role, app_pwd):
        """Email committee member"""
        self.email_people(subject, input_message, [
                          committee_role + '@sjcjcr.com'], app_pwd=app_pwd)
        return "Emailed {}".format(self[committee_role]['name'])

    def email_committee(self, subject, input_message, app_pwd):
        """Email entire committee"""
        committee_emails = [role + '@sjcjcr.com' for role in self.keys()]
        self.email_people(subject, input_message, committee_emails)
        return "Emailed JCR Committee"

    def email_someone(self, subject, input_message, email_address, app_pwd):
        """Email committee member"""
        self.email_people(subject, input_message, [email_address])
        return "Emailed {}".format(email_address)

    def email_people(self, subject, input_message, address_list, app_pwd, reply_to=None, attachment=None):
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
            file_content = retrieveBinary(attachment)
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file_content)

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                "attachment; filename= {}".format(attachment),
            )

            # Add attachment to message and convert message to string
            message.attach(part)

        '''# TODO: implement actual env file
        with open(os.path.join(script_dir, "config.txt"), "r") as file:
            # See https://support.google.com/accounts/answer/185833?hl=en
            app_key = file.readlines()[0]

        gmail_pwd = app_key  # App password not re-usable see above.'''
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(gmail_user, app_pwd)
        smtpserver.sendmail(gmail_user, address_list, message.as_string())
        smtpserver.close()
        return "Email sent!"
