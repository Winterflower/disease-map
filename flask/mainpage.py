__author__ = 'winterflower'
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/visualise')
def visualization():
    return "Now generating your visualization"

@app.route('/upload_csv')
def upload_csv():
    return render_template("test_upload.html")



if __name__ == '__main__':
    app.run()
