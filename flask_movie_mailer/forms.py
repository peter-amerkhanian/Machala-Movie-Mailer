from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_movie_mailer.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=20)],
                       render_kw={"placeholder": "Name"})
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()],
                        render_kw={"placeholder": "Email"})
    location = SelectField('Location',
                           choices=[("Machala", "Machala")],
                           validators=[DataRequired()])
    frequency = SelectField('Frequency',
                            choices=[(0, "How often would you like to receive emails..."),
                                     ("Daily", "Daily"),
                                     ("Weekends", "Only on weekends")],
                            validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already connected to an account')

    def validate_frequency(self, frequency):
        if frequency.data == 0:
            raise ValidationError('Please select how often you want to be emailed')


class UnsubscribeForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()],
                        render_kw={"placeholder": "Email"})
    unsubscribe = SubmitField('Unsubscribe')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("That email isn't connected to an account")