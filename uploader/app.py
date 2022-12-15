import flask
import uuid

from flask import request, jsonify, send_from_directory
from os import listdir
from os.path import join, dirname, abspath


BASEDIR = abspath(dirname(__file__))
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ('txt', 'md', 'pdf', 'png', 'jpg', 'jpeg', 'gif')

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'status': 'No file'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'File not selected', 'filename': None})
    if file and allowed_file(file.filename):
        filename, *other = file.filename.split('.')
        unique_id = uuid.uuid4().hex
        filename = '.'.join(['-'.join([filename, unique_id]), *other])
        file.save(join(BASEDIR, app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'status': 'OK', 'filename': filename})
    return jsonify({'status': 'Invalid file extension', 'filename': None})


@app.route('/check/<string:filename>', methods=['GET'])
def check(filename):
    uploaded_files = set(listdir(join(BASEDIR, app.config['UPLOAD_FOLDER'])))
    status = 'found' if filename in uploaded_files else 'not found'
    return jsonify({'status': status, 'filename': filename})


@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(
        join(join(BASEDIR, app.config['UPLOAD_FOLDER'])), filename
    )


if __name__ == '__main__':
    app.run()
