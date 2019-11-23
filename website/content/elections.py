import os
from flask import send_file
from website.content.retrieve import retrieveJson

curr_dir = os.path.dirname(__file__)

"""
    ELECTIONS_ONGOING variable allows switching between two slightly different
    templates, since for an ongoing election you want several people for each
    position and different header text. You will also want to put the voting
    link for the election in the heading paragraph as it becomes available.
    For this you'll need to edit currentelections.j2.html, see comments in HTML
"""

# TODO: Do this in .env file
ELECTIONS_ONGOING = True

if ELECTIONS_ONGOING:
    json_path = 'elections/candidates'
else:
    json_path = 'elections/elected'

election_json = retrieveJson(json_path)

def get_manifesto(filename):
    """Sends manifesto as attachment"""
    filepath = os.path.join(curr_dir, 'elections/manifestos', filename)
    return send_file(filepath, as_attachment=True)
