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

#johnian_crsids.remove('jfc43') #Testing login works

johnian_access = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 15,
                                            require_principal = johnian_crsids)

class Committee(dict):
    '''To do: edit .forward function.
        Send PDF minutes, maybe have separate Committee Flask app? (committee.sjcjcr.com)'''
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
                        print(type(item2))
                        if isinstance(item2, dict):
                            print('Woop')
                            self.committee_crsids.append(item2['crsid'])
        self.committee_crsids = set(self.committee_crsids)

    def email_member(self, input_message, committee_role):
        self.email_people(input_message, [committee_role])
        return "Emailed {}".format(self[committee_role]['name'])

    def email_all(self, input_message):
        return self.email_people(input_message, self.keys())

    def email_people(self, input_message, committee_roles):
        committee_emails = [role + '@sjcjcr.com' for role in committee_roles]
        recipients_string = ", ".join(committee_emails)
        gmail_user = 'sjcjcrmisc@gmail.com'
        gmail_pwd = '***REMOVED***'  # One-off password, not re-usable
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + recipients_string + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:EmailTest \n'
        input_message = input_message
        msg = header + input_message
        smtpserver.sendmail(gmail_user, committee_emails, msg)
        smtpserver.close()
        return "Emailed JCR Committee"

JCR = Committee("content/committee.json")

committee_access = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 15,
                                            require_principal = JCR.committee_crsids)
#print(JCR['PRESIDENT']['name'])
#print(JCR['COMPUTING']['name'])

#print(JCR.email_member('Function for emailing members','computing')) # Pls don't spam meh
