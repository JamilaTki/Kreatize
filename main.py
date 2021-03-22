from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

import trimesh

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
        if not allowed_file(file.filename):
            flash('Please select a file within the supported formats: {0}'.format(
                ", ".join(map(str, app.config['ALLOWED_EXTENSIONS']))))
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file_path = (os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            file.save(file_path)
            return redirect(url_for('uploaded_file',
                                    file_path=file_path))
    return render_template('index.html', title='upload_file')


@app.route('/uploads/<file_path>')
def uploaded_file(file_path):
    data = extract_data(file_path)
    return render_template('display_data.html', data=data)


def extract_data(file_path):
    my_mesh = trimesh.load(file_path)
    data = {
        'volume': round(my_mesh.volume, 2),
        'area': round(my_mesh.area, 2),
        'bounding_sphere':
            {
                'center': [round(x, 2) for x in my_mesh.bounding_sphere.centroid],
                'diameter': round(my_mesh.bounding_sphere.extents[0], 2)
            },
        'bounding_cylinder':
            {
                'center': [round(x, 2) for x in my_mesh.bounding_cylinder.centroid],
                'diameter': round(my_mesh.bounding_cylinder.extents[0], 2),
                'height': round(my_mesh.bounding_cylinder.extents[2], 2)
            },
        'bounding_box':
            {
                'center': [round(x, 2) for x in my_mesh.bounding_box_oriented.centroid],
                'length': round(my_mesh.bounding_box_oriented.extents[0], 2),
                'width': round(my_mesh.bounding_box_oriented.extents[1], 2),
                'height': round(my_mesh.bounding_box_oriented.extents[2], 2)
            },
        'bounding_cube': {
            'edge': round(max(my_mesh.bounding_box_oriented.extents.tolist()), 2)
        }
    }
    return data


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
