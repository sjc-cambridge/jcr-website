"""Module for sending pdf documents to client"""
import os
from flask import send_file
from website.helper.johnians import update_johnian_crsids
curr_dir = os.path.dirname(__file__)


def send_helpdoc():
    """Sends transparency doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/GettingHelp.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename="JCR - Getting Help.pdf")

def send_transparencydoc():
    """Sends transparency doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/JCRTransparencyDoc.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename="JCRTransparency.pdf")

def send_constitution():
    """Sends constitution doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/Constitution.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename="JCRConstitution.pdf")

def send_billsglossary():
    """Sends constitution doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/StudentBillsGlossary.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename="Student Bills Glossary.pdf")

def send_johnianlist():
    update_johnian_crsids()
    filepath = os.path.join(curr_dir, "config/johnians.txt")
    return send_file(filepath, as_attachment=True, attachment_filename="JohnianList.txt")
