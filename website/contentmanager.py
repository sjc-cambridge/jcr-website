import os
from flask import send_file
import json

curr_dir = os.path.dirname(__file__)


"""
    ELECTIONS_ONGOING variable allows switching between two slightly different
    templates, since for an ongoing election you want several people for each
    position and different header text. You will also want to put the voting
    link for the election in the heading paragraph as it becomes available.
    For this you'll need to edit currentelections.j2.html, see comments in HTML
"""

ELECTIONS_ONGOING = False

if ELECTIONS_ONGOING:
    json_path = 'content/elections/candidates.json'
else:
    json_path = 'content/elections/elected.json'

election_json_path = os.path.join(curr_dir, json_path)
with open(election_json_path, 'r') as f:
    election_json = json.load(f)

def get_manifesto(filename):
    filepath = os.path.join(curr_dir,'content/elections/manifestos', filename)
    return send_file(filepath)

def get_minutes(filename):
    filepath = os.path.join(curr_dir,'content/minutes', filename+'.pdf')
    return send_file(filepath, attachment_filename='Minutes.pdf')

def get_transparencydoc():
    filename = "JCRTransparencyDoc.pdf"
    filepath = os.path.join(curr_dir,'content', filename)
    return send_file(filepath, attachment_filename='JCRTransparency.pdf')
