import os
from flask import send_file

curr_dir = os.path.dirname(__file__)


def send_transparencydoc():
    filepath = os.path.join(curr_dir, "documents/JCRTransparencyDoc.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename="JCRTransparency.pdf")


def send_constitution():
    filepath = os.path.join(curr_dir, "documents/Constitution.pdf")
    return send_file(filepath,  as_attachment=True, attachment_filename="JCRConstitution.pdf")