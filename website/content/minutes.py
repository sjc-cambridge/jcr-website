import os
from flask import send_file
import json
from werkzeug.utils import secure_filename
from website.helper.timehelper import get_year_range
import pathlib
from website.content.retrieve import retrieveJson

curr_dir = os.path.dirname(__file__)

def save_minutes(term, year, file):
    yearpath = os.path.join(curr_dir, 'minutes', year)
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
    filepath = os.path.join(curr_dir, 'minutes', year, term, filename)
    try:
        os.remove(filepath)
        termpath = os.path.join(curr_dir, 'minutes', year, term)
        if not os.listdir(termpath):
            os.rmdir(termpath)  # Delete term folder if now empty
        return 'Deleted minutes'
    except Exception as e:
        print(e)


def get_minutes_dict():
    """Get minutes folder directory structure for displaying stuff in minutes.j2.html"""
    minutes_dict = dict()
    minutes_range = get_year_range()
    minutes_path = pathlib.Path(os.path.join(curr_dir, 'minutes'))
    for academic_year in minutes_path.iterdir():
        year_str = str(academic_year).split('/')[-1]  # Strip rest of file path
        if year_str in minutes_range:
            minutes_dict[year_str] = dict()
            year_path = pathlib.Path(str(academic_year))
            for term in year_path.iterdir():
                term_str = str(term).split('/')[-1]  # Strip rest of file path
                minutes_dict[year_str][term_str] = []
                meeting_path = pathlib.Path(str(term))
                for meeting in meeting_path.iterdir():
                    meeting_str = str(meeting).split('/')[-1]
                    minutes_dict[year_str][term_str].append(meeting_str)
    return minutes_dict


def get_minutes(term, year, filename):
    filepath = os.path.join(curr_dir, 'minutes', year, term, filename)
    return send_file(filepath, as_attachment=True)


def get_transparencydoc():
    filepath = os.path.join(curr_dir, "minutes/JCRTransparencyDoc.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename='JCRTransparency.pdf')
