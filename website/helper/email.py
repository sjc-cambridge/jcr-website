"""Email helper file used to send emails"""
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from website.content.retrieve import retrieveBinary

script_dir = os.path.dirname(__file__)


def email_someone(subject, input_message, email_address):
    """Email committee member"""
    email_people(subject, input_message, [email_address])
    return "Emailed {}".format(email_address)


def email_people(subject, input_message, address_list, reply_to=None, attachment=None):
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

    # TODO: implement actual env file
    with open(os.path.join(script_dir, "config.txt"), "r") as file:
        # See https://support.google.com/accounts/answer/185833?hl=en
        app_key = file.readlines()[0]

    gmail_pwd = app_key  # App password not re-usable see above.
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(gmail_user, gmail_pwd)
    smtpserver.sendmail(gmail_user, address_list, message.as_string())
    smtpserver.close()
    return "Email sent!"
