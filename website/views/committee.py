from flask import Blueprint, render_template, send_file, request, redirect, url_for, flash
import os
from website.helper.auth import committee_access, JCR
from website.content.minutes import get_minutes, save_minutes, get_minutes_dict, delete_minutes
from website.helper.timehelper import get_year_range
import datetime

committee = Blueprint('committee', __name__, url_prefix="/committee")

"""
Things for committee page:
- Allow committee to add/edit/remove agenda points, probably store in weekly JSON.
- Ability for Martin to upload resulting minutes straight into content folder would be ideal.
- This could simultaneously email it out to committee members and the beauty of jinja would
    mean it would appear on the minutes of meetings page.
"""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@committee.route("/")
@committee_access
def committee_home():
    return render_template("committee/home.j2.html", crsid=committee_access.principal,
                            current_page ="/committee/home", JCR=JCR)

@committee.route("/agenda")
@committee_access
def committee_agenda():
    return render_template("committee/agenda.j2.html", crsid=committee_access.principal,
                            current_page ="/committee/agenda", JCR=JCR)


@committee.route("/upload_minutes", methods=['GET', 'POST'])
@committee_access
def upload_minutes():
    if request.method == 'POST':
        if committee_access.principal not in (JCR['secretary']['crsid'], JCR['computing']['crsid']):
            print('hey')
            flash('Only the secretary or computing officer can add/remove minutes!')
            return redirect(request.url)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            year = request.form.get("year")
            term = request.form.get("term")
            log_msg = save_minutes(term, year, file)
            flash(log_msg)
            return redirect(request.url)
    minutes_dict = get_minutes_dict()
    minutes_range = get_year_range()  # Range of minutes that can be added
    return render_template("committee/upload_minutes.j2.html", crsid=committee_access.principal,
                            JCR=JCR, minutes_dict=minutes_dict,
                            sorted=sorted, minutes_range=minutes_range)



@committee.route('/delete_minutes')
@committee_access
def minutes_page():
    if committee_access.principal not in (JCR['secretary']['crsid'], JCR['computing']['crsid']):
        secretary_name, computing_name = JCR['secretary']['name'], JCR['computing']['name']
        flash('Only the Secretary ({0}) or Computing officer ({1}) can add/remove minutes!'.format(secretary_name, computing_name))
        return redirect(url_for('committee.upload_minutes'))
    academicyear = request.args.get("academicyear") # e.g. 2019/2020
    term = request.args.get("term")
    filename = request.args.get("filename")
    try:
        delete_minutes(term, academicyear, filename)
    except Exception as e:
        print(e)
    return redirect(url_for('committee.upload_minutes'))
