from flask import Blueprint, render_template, send_file, request
import os
from website.config import committee_access, JCR
from website.contentmanager import get_minutes, get_transparencydoc, get_manifesto, election_json, ELECTIONS_ONGOING


committee = Blueprint('committee', __name__)

@committee.route("/committee")
@committee.route("/committee/")
@committee.route("/committee/home")
@committee_access
def committee_home():
    user_crsid = johnian_access.principal
    return render_template("committee/home.j2.html", crsid=johnian_access.principal, current_page="/committee")
