__author__ = 'winterflower'
import os
from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import autoload_server
from visualization import generate_figure, getMap

app = Flask(__name__)

# Global variables for CSV file upload
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOADED_FILES = os.listdir(UPLOAD_FOLDER)


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
    return redirect(url_for('data_page'))


@app.route('/visualise')
def visualization():

    # FIXME: do not hardcode the csv file path
    tag = autoload_server(*getMap(UPLOADED_FILES[0]))

    return render_template('app.html', map=tag)

if __name__ == '__main__':
    app.run(debug=True)
