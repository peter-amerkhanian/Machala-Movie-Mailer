from flask import render_template, url_for, flash, redirect, Markup, request, session
from flask_movie_mailer import app, db
from flask_movie_mailer.forms import RegistrationForm, UnsubscribeForm
from flask_movie_mailer.models import User
from flask_movie_mailer.quote_generator import generate_random_quote
from flask_movie_mailer.movie_today import get_movie_today
from datetime import datetime


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
        session['city'] = form.location.data
        return redirect(url_for('registered'))
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/registered")
def registered():
    now = datetime.utcnow().hour
    if now > 13:
        return render_template('registered.html',
                               message=Markup(get_movie_today(session['city'])))
    else:
        return render_template('registered.html',
                               message=Markup('<p>Your first email will arrive at 9:00am</p>'))


@app.route("/unsubscribe", methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('unsubscribed'))
    return render_template('unsubscribe.html',
                           title='Login',
                           form=form)


@app.route("/unsubscribed")
def unsubscribed():
    quote = generate_random_quote()
    return render_template('unsubscribed.html',
                           text=quote["text"],
                           author=quote["author"])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('errors/404.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500
