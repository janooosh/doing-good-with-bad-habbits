# app.py
from flask import Flask, render_template, request   
from ourupload import doupload
from cleaning_new import clean

app = Flask(__name__)    

UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER         

@app.route("/")   
def hello():                                   
    return render_template('FileUpload.html')        

# POST Route
# (1) Receive uploaded file from FileUpload.html Form (DONE)
# (2) Python function that returns the file something
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      bank = request.form.get('bankselect')
      #return(str(bank))

      f = request.files['file']
      f.save(f.filename)
      result = clean(f.filename,bank)
      return result
