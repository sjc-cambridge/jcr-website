"""Module for manipulating minutes pdf documents from JCR meetings"""

import os
from flask import send_file
import json
from werkzeug.utils import secure_filename
from website.helper.timehelper import get_year_range
import pathlib
from website.content.retrieve import retrieveJson
from website.paths import PRIV_DIR

MINUTES_DIR = os.path.join(PRIV_DIR, "minutes")


def save_minutes(term, year, file):
    """
    Saves minutes pdf in correct directory
    year: int
    term: {'Michaelmas', 'Lent', 'Easter'}
    file: Minutes pdf to save
    """
    yearpath = os.path.join(MINUTES_DIR, year)
    if not os.path.exists(yearpath):
        os.makedirs(yearpath)
    termpath = os.path.join(yearpath, term)
    if not os.path.exists(termpath):
        os.makedirs(termpath)
    filename = secure_filename(file.filename)
    filepath = os.path.join(termpath, filename)
    try:
        file.save(filepath)
        return "Saved minutes"
    except Exception as e:
        print(e)


def delete_minutes(term, year, filename):
    """
    Deletes set of minutes from server
    """
    filepath = os.path.join(MINUTES_DIR, year, term, filename)
    try:
        os.remove(filepath)
        termpath = os.path.join(MINUTES_DIR, year, term)
        if not os.listdir(termpath):
            os.rmdir(termpath)  # Delete term folder if now empty
        return "Deleted minutes"
    except Exception as e:
        print(e)


def get_minutes_dict():
    """Get minutes folder directory structure for displaying stuff in minutes.j2.html"""
    minutes_dict = dict()
    minutes_range = get_year_range(4)
    minutes_path = pathlib.Path(MINUTES_DIR)
    for academic_year in minutes_path.iterdir():
        year_str = str(academic_year).split("/")[-1]  # Strip rest of file path
        if year_str in minutes_range:
            minutes_dict[year_str] = dict()
            year_path = pathlib.Path(str(academic_year))
            for term in year_path.iterdir():
                term_str = str(term).split("/")[-1]  # Strip rest of file path
                minutes_dict[year_str][term_str] = []
                meeting_path = pathlib.Path(str(term))
                for meeting in meeting_path.iterdir():
                    meeting_str = str(meeting).split("/")[-1]
                    minutes_dict[year_str][term_str].append(meeting_str)
    return minutes_dict


def get_minutes(term, year, filename):
    """Send minutes pdf as attachment"""
    filepath = os.path.join(MINUTES_DIR, year, term, filename)
    return send_file(filepath, as_attachment=True)
