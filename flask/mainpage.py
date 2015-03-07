__author__ = 'winterflower'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/visualise')
def visualization():
    return "Now generating your visualization"


if __name__ == '__main__':
    app.run()