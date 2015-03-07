__author__ = 'winterflower'
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/visualise')
def visualization():
    return "Now generating your visualization"


# Global variables for CSV file upload
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

# Check allowed extensions:
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_page')
def upload_page():
    return render_template("test_upload.html")

@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))



if __name__ == '__main__':
    app.run(debug=True)
