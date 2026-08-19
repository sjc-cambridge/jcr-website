"""Module for manipulating transparency documents"""

import os
from flask import send_file
import json
from werkzeug.utils import secure_filename
from website.helper.timehelper import get_year_range
import pathlib
from website.content.retrieve import retrieveJson
from website.paths import PRIV_DIR

TRANSPARENCY_DIR = os.path.join(PRIV_DIR, "transparency")


def save_transparency(term, year, file):
    """
    Saves transparency doc pdf in correct directory
    year: int
    term: {'Michaelmas', 'Lent', 'Easter'}
    file: Transparency pdf to save
    """
    yearpath = os.path.join(TRANSPARENCY_DIR, year)
    if not os.path.exists(yearpath):
        os.makedirs(yearpath)
    termpath = os.path.join(yearpath, term)
    if not os.path.exists(termpath):
        os.makedirs(termpath)
    filename = secure_filename(file.filename)
    filepath = os.path.join(termpath, filename)
    try:
        file.save(filepath)
        return "Saved transparency document"
    except Exception as e:
        print(e)


def delete_transparency(term, year, filename):
    """
    Deletes a transparency doc from server
    """
    filepath = os.path.join(TRANSPARENCY_DIR, year, term, filename)
    try:
        os.remove(filepath)
        termpath = os.path.join(TRANSPARENCY_DIR, year, term)
        if not os.listdir(termpath):
            os.rmdir(termpath)  # Delete term folder if now empty
        return "Deleted transparency document"
    except Exception as e:
        print(e)


def get_transparency_dict():
    """Get transparency doc folder directory structure for displaying stuff in transparency.j2.html"""
    transparency_dict = dict()
    transparency_range = get_year_range(4)
    transparency_path = pathlib.Path(TRANSPARENCY_DIR)
    for academic_year in transparency_path.iterdir():
        year_str = str(academic_year).split("/")[-1]  # Strip rest of file path
        if year_str in transparency_range:
            transparency_dict[year_str] = dict()
            year_path = pathlib.Path(str(academic_year))
            for term in year_path.iterdir():
                term_str = str(term).split("/")[-1]  # Strip rest of file path
                transparency_dict[year_str][term_str] = []
                meeting_path = pathlib.Path(str(term))
                for meeting in meeting_path.iterdir():
                    meeting_str = str(meeting).split("/")[-1]
                    transparency_dict[year_str][term_str].append(meeting_str)
    return transparency_dict


def get_transparency(term, year, filename):
    """Send transparency doc pdf as attachment"""
    filepath = os.path.join(TRANSPARENCY_DIR, year, term, filename)
    return send_file(filepath, as_attachment=True)
