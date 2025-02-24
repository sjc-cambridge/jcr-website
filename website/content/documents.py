"""Module for sending pdf documents to client"""
import os
from flask import send_file
from website.helper.johnians import update_johnian_crsids
curr_dir = os.path.dirname(__file__)


def send_helpdoc():
    """Sends transparency doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/GettingHelp.pdf")
    return send_file(filepath,  as_attachment=False, attachment_filename="JCR - Getting Help.pdf")

def send_constitution():
    """Sends constitution doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/Constitution.pdf")
    return send_file(filepath,  as_attachment=False, attachment_filename="JCRConstitution.pdf")

def send_billsglossary():
    """Sends bills glossary doc as pdf attachment"""
    filepath = os.path.join(curr_dir, "documents/StudentBillsGlossary.pdf")
    return send_file(filepath,  as_attachment=False, attachment_filename="Student Bills Glossary.pdf")

def send_financialaid():
    """Sends financial aid doc as pdf"""
    filepath = os.path.join(curr_dir, "documents/FinancialAidDocument.pdf")
    return send_file(filepath,  as_attachment=False, attachment_filename="Financial Aid.pdf")

def send_financialaid_spreadsheet():
    """Sends financial aid spreadsheet as pdf"""
    filepath = os.path.join(curr_dir, "documents/FinancialAidSpreadsheet.pdf")
    return send_file(filepath,  as_attachment=False, attachment_filename="Financial Aid Spreadsheet.pdf")

def send_johnianlist():
    #update_johnian_crsids()
    filepath = os.path.join(curr_dir, "config/johnians.txt")
    return send_file(filepath, as_attachment=True, attachment_filename="JohnianList.txt")

def send_fresherguide():
    """Sends freshers guide doc as pdf"""
    filepath = os.path.join(curr_dir, "documents/FreshersGuide.pdf")
    return send_file(filepath,  as_attachment=False, attachment_filename="Fresher's guide.pdf")