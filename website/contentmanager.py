import os
from flask import send_file
import json
from werkzeug.utils import secure_filename
from website.misc import get_year_range
import pathlib
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

def delete_minutes(term, year, filename):
    filepath = os.path.join(curr_dir,'content/minutes', year, term, filename)
    try:
        os.remove(filepath)
        termpath = os.path.join(curr_dir,'content/minutes', year, term)
        if not os.listdir(termpath):
            os.rmdir(termpath)  # Delete term folder if now empty
        return 'Deleted minutes'
    except Exception as e:
        print(e)

def get_minutes_dict():
    """Get minutes folder directory structure for displaying stuff in minutes.j2.html"""
    minutes_dict = dict()
    minutes_range = get_year_range()
    minutes_path = pathlib.Path(os.path.join(curr_dir,'content/minutes'))
    for academic_year in minutes_path.iterdir():
        year_str = str(academic_year).split('/')[-1] # Strip rest of file path
        if year_str in minutes_range:
            minutes_dict[year_str] = dict()
            year_path = pathlib.Path(str(academic_year))
            for term in year_path.iterdir():
                term_str = str(term).split('/')[-1] # Strip rest of file path
                minutes_dict[year_str][term_str] = []
                meeting_path = pathlib.Path(str(term))
                for meeting in meeting_path.iterdir():
                    meeting_str = str(meeting).split('/')[-1]
                    minutes_dict[year_str][term_str].append(meeting_str)
    return minutes_dict

def get_minutes(term, year, filename):
    filepath = os.path.join(curr_dir,'content/minutes', year, term, filename)
    return send_file(filepath, as_attachment=True)

def get_transparencydoc():
    filename = "JCRTransparencyDoc.pdf"
    filepath = os.path.join(curr_dir,'content', filename)
    return send_file(filepath,  as_attachment=True, attachment_filename='JCRTransparency.pdf')
