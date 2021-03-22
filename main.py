from flask import Flask
from flask import render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'
app.config['ALLOWED_EXTENSIONS'] = ['stl']


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file or submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_path = (os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            file.save(file_path)
    return render_template('index.html', title='upload_file')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
