import ucam_webauth
import ucam_webauth.raven
import ucam_webauth.raven.flask_glue
import pickle, requests, json
from website.helper.committee import Committee
from website.helper.johnians import retrieve_johnian_crsids

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

# set of all johnian crsids
johnian_crsids = retrieve_johnian_crsids()

# This decorator restricts pages to Johnians
johnian_access = ucam_webauth.raven.flask_glue.AuthDecorator(
    max_life=6000,
    require_principal=johnian_crsids
)

# JCR object to be exported
JCR = Committee()

# Committee access decorator restricts access to just committee members
committee_access = ucam_webauth.raven.flask_glue.AuthDecorator(
    max_life=6000,
    require_principal=JCR.committee_crsids
)


def is_human(captcha_response):
    """ Validating recaptcha response from google server.
        Returns True captcha test passed for the submitted form
        else returns False.
    """
    secret = "***REMOVED***"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']
