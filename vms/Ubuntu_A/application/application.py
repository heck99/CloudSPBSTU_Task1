from flask import request
from flask import Flask
from crypt import methods

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_word():
	return "<p>Hello, Word!</p>\n"


@app.route("/change_login", methods=['PUT'])
def change_login():
	return f"<p>new login is {request.form['login']}!</p>\n"


@app.route("/login", methods=['POST'])
def login():
	return f"<p>Your login is {request.form['login']}</p>\n"

app.run(host='0.0.0.0', port=5000)
