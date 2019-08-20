import os
from flask import send_file

curr_dir = os.path.dirname(__file__)


def get_minutes(filename):
    filepath = os.path.join(curr_dir,'minutes', filename+'.pdf')
    try:
        return send_file(filepath, attachment_filename='Minutes.pdf')
    except Exception as e:
        print(e)
        return None
