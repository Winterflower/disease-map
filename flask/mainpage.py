__author__ = 'winterflower'
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global variables for CSV file upload
UPLOAD_FOLDER = '/home/eleonore/Documents/fb_hack_2015/disease-map/flask/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOADED_FILES = []


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data_page')
def data_page():
    files = UPLOADED_FILES
    return render_template("user_page.html", files=files)


# Check allowed extensions:
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_page', methods=['GET', 'POST'])
def upload_page():
    return render_template("test_upload.html")


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            print os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            UPLOADED_FILES.append(filename)
            #return redirect(url_for('uploaded_file', filename=filename))
    return redirect(url_for('data_page'))


@app.route('/visualise')
def visualization():
    return "Now generating your visualization"



if __name__ == '__main__':
    app.run(debug=True)
