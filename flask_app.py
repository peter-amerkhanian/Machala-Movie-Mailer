from flask import Flask, render_template, Markup
from filter_info import mail

app = Flask(__name__)


@app.route("/")
def test():
    return render_template('index.html', mail=mail)


if __name__ == "__main__":
    app.run()