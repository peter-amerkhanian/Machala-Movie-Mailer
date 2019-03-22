from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, widgets, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_movie_mailer.models import User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already connected to an account')


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