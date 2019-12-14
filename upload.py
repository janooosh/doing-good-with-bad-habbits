import os

from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/upload'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
    return '''<!doctype html>
              <title>Upload new File</title>
              <h1>Upload new File</h1>
              <form action="" method=post enctype=multipart/form-data>
                <p><input type=file name=file>
                <input type=submit value=Upload>
              </form>'''

if __name__ == '__main__':
    app.run()