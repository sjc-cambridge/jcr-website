from flask import Blueprint, render_template, send_file, request, redirect, url_for, flash
import os
from website.config import committee_access, JCR
from website.contentmanager import get_minutes, save_minutes


committee = Blueprint('committee', __name__)

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

@committee.route("/committee", methods=['GET', 'POST'])
@committee.route("/committee/", methods=['GET', 'POST'])
@committee_access
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(request.files)
            year = request.form.get("year")
            term = request.form.get("term")
            print(year, term)
            log_msg = save_minutes(term, year, file)
            flash(log_msg)
            return redirect(url_for('committee.upload_file'))
    return '''
    <!doctype html>
    <title>Upload Minutes</title>
    <h1>Upload Minutes</h1>
    <form method=post enctype=multipart/form-data>
      <select name="year">
          <option value="2018-2019">2018/2019</option>
          <option value="2019-2020">2019/2020</option>
      </select>
      <select name="term">
          <option value="Michaelmas">Michaelmas</option>
          <option value="Lent">Lent</option>
          <option value="Easter">Easter</option>
      </select>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
