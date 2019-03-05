from flask import render_template, url_for, flash, redirect, Markup
from flask_movie_mailer import app, db
from flask_movie_mailer.forms import RegistrationForm, UnsubscribeForm
from flask_movie_mailer.models import User
from flask_movie_mailer.quote_generator import generate_random_quote


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
        flash("Account created for {}.".format(form.email.data), "success")
        return redirect(url_for('home'))
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/unsubscribe", methods=['GET', 'POST'])
def unsubscribe():
    form = UnsubscribeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        db.session.delete(user)
        db.session.commit()
        quote = generate_random_quote()
        flash(Markup(
            """
           <b>{} has been unsubscribed... <i class="em em-cry"></i></b> <br/>
           <p></p>
        <div class="center">
           <i>"{}"</i> <br/>
           <sub>{}</sub>
        </div>
            """.format(form.email.data, quote["text"], quote["author"])))
        return redirect(url_for('home'))
    return render_template('unsubscribe.html',
                           title='Login',
                           form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('errors/404.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500
