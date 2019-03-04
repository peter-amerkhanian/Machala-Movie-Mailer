from flask import render_template, url_for, flash, redirect
from flask_movie_mailer import app, db
from flask_movie_mailer.forms import RegistrationForm, LoginForm
from flask_movie_mailer.models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    location=form.location.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.email.data}.", "success")
        return redirect(url_for('home'))
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"{form.email.data} has been unsubscribed", "success")
        return redirect(url_for('home'))
    return render_template('login.html',
                           title='Login',
                           form=form)
