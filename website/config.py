import ucam_webauth
import ucam_webauth.raven
import ucam_webauth.raven.flask_glue
import os
import pickle
import smtplib
import json

script_dir = os.path.dirname(__file__)

with open(os.path.join(script_dir, "johnians.txt"), "rb") as file:
    johnian_crsids = set(pickle.load(file))

#johnian_crsids.remove('jfc43') #Testing login works by removing myself

"""This decorator restricts pages to Johnians."""
johnian_access = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 15,
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

    def email_people(self, subject, input_message, address_list):
        """Email a list of emails a subject/ input message. Gmail account uses
            2-factor authentication so password used won't work anywhere else."""
        recipients_string = ", ".join(address_list)
        gmail_user = 'sjcjcrmisc@gmail.com'
        gmail_pwd = '***REMOVED***'  # See https://support.google.com/accounts/answer/185833?hl=en
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + recipients_string + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:' + subject + '\n\n'
        input_message = input_message
        msg = header + input_message
        smtpserver.sendmail(gmail_user, address_list, msg)
        smtpserver.close()
        return "Emailed sent!"

JCR = Committee("content/committee.json")

# Committee access decorator for restricting committee section of website.
committee_access = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 15,
                                            require_principal = JCR.committee_crsids)
#print(JCR['PRESIDENT']['name'])
#print(JCR['COMPUTING']['name'])

#print(JCR.email_member("St. John's Emailer", "Here are last weeks minutes",'computing')) # Pls don't spam meh
