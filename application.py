from flask import Flask

app = Flask(__name__)

@app.route("/get")
def hello_word_get():
	return "<p>Hello, Word from get!</p>"


@app.route("/put")
def hello_word_put():
	return "<p>Hello, Word from put!</p>"


@app.route("/post")
def hello_word_pust():
	return "<p>Hello, Word from post!</p>"

app.run(host='0.0.0.0', port=5000)
