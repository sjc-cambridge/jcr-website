from flask import Blueprint, render_template, send_file, request
import os
from website.config import committee_access, JCR
from website.contentmanager import get_minutes, get_transparencydoc, get_manifesto, election_json, ELECTIONS_ONGOING


committee = Blueprint('committee', __name__)

"""
Things for committee page:
- Allow committee to add/edit/remove agenda points, probably store in weekly JSON.
- Ability for Martin to upload resulting minutes straight into content folder would be ideal.
- This could simultaneously email it out to committee members and the beauty of jinja would
    mean it would appear on the minutes of meetings page.
"""

@committee.route("/committee")
@committee.route("/committee/")
@committee.route("/committee/home")
@committee_access
def committee_home():
    user_crsid = johnian_access.principal
    return render_template("committee/home.j2.html", crsid=johnian_access.principal, current_page="/committee")
