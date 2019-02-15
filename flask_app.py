from flask import Flask, render_template, Markup

app = Flask(__name__)
with open("mail.txt", "r") as file:
    mail = Markup(file.readline())


@app.route("/")
def test():
    return render_template('index.html', mail=mail)


if __name__ == "__main__":
    app.run()