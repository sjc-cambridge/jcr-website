import os
from flask import send_file
import json

curr_dir = os.path.dirname(__file__)

ELECTIONS_ONGOING = True

if ELECTIONS_ONGOING:
    json_path = 'content/elections/candidates.json'
else:
    json_path = 'content/elections/elected.json'

election_json_path = os.path.join(curr_dir, json_path)
with open(election_json_path, 'r') as f:
    election_json = json.load(f)

def get_manifesto(filename):
    filepath = os.path.join(curr_dir,'content/manifestos', filename)
    try:
        return send_file(filepath)
    except Exception as e:
        print(e)
        return None

def get_minutes(filename):
    filepath = os.path.join(curr_dir,'content/minutes', filename+'.pdf')
    try:
        return send_file(filepath, attachment_filename='Minutes.pdf')
    except Exception as e:
        print(e)
        return None

def get_transparencydoc():
    filename = "JCRTransparencyDoc.pdf"
    filepath = os.path.join(curr_dir,'content', filename)
    try:
        return send_file(filepath, attachment_filename='JCRTransparency.pdf')
    except Exception as e:
        print(e)
        return None
