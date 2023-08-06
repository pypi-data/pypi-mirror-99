from flask import Flask
# set / export FLASK_ENV = development
# set / export FLASK_APP = hello
# run -p 5002

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

