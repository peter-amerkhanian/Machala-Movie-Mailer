from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=20)],
                       render_kw={"placeholder": "Name"})
    email = StringField('Email:',
                        validators=[DataRequired(),
                                    Email()],
                        render_kw={"placeholder": "Email"})
    location = SelectField('Location:',
                           choices=[("machala", "Machala"), ("cuenca", "Cuenca"), ("quito", "Quito")],
                           validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=20)],
                       render_kw={"placeholder": "Name"})
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()],
                        render_kw={"placeholder": "Email"})
    unsubscribe = SubmitField('Unsubscribe')