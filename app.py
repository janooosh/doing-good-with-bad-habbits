# app.py
from flask import Flask, render_template, request   
from ourupload import doupload
app = Flask(__name__)             

@app.route("/")   
def hello():                                   
    return render_template('FileUpload.html')        

# POST Route
# (1) Receive uploaded file from FileUpload.html Form (DONE)
# (2) Python function that returns the file something
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      testf = doupload(f)
      return testf