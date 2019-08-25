import os
from flask import send_file
import json
from werkzeug.utils import secure_filename

curr_dir = os.path.dirname(__file__)

"""
    ELECTIONS_ONGOING variable allows switching between two slightly different
    templates, since for an ongoing election you want several people for each
    position and different header text. You will also want to put the voting
    link for the election in the heading paragraph as it becomes available.
    For this you'll need to edit currentelections.j2.html, see comments in HTML
"""

ELECTIONS_ONGOING = True

if ELECTIONS_ONGOING:
    json_path = 'content/elections/candidates.json'
else:
    json_path = 'content/elections/elected.json'

election_json_path = os.path.join(curr_dir, json_path)
with open(election_json_path, 'r') as f:
    election_json = json.load(f)

def get_manifesto(filename):
    filepath = os.path.join(curr_dir,'content/elections/manifestos', filename)
    return send_file(filepath, as_attachment=True)


def save_minutes(term, year, file):
    if '' in [term, year]:
        return ("Term or academic year not specified, please try again.")
    yearpath = os.path.join(curr_dir,'content/minutes', year)
    if not os.path.exists(yearpath):
        os.makedirs(yearpath)
    termpath = os.path.join(yearpath, term)
    if not os.path.exists(termpath):
        os.makedirs(termpath)
    filename = secure_filename(file.filename)
    filepath = os.path.join(termpath, filename)
    try:
        file.save(filepath)
        return 'Saved minutes'
    except Exception as e:
        print(e)


def get_minutes(term, year, filename):
    filepath = os.path.join(curr_dir,'content/minutes', year, term, filename)
    return send_file(filepath, as_attachment=True, attachment_filename='Minutes.pdf')

def get_transparencydoc():
    filename = "JCRTransparencyDoc.pdf"
    filepath = os.path.join(curr_dir,'content', filename)
    return send_file(filepath,  as_attachment=True, attachment_filename='JCRTransparency.pdf')
