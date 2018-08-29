from wtforms import Form, PasswordField, StringField, RadioField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, EqualTo, NumberRange, Email, Length


class RegisterForm(Form):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    tel = StringField('Telephone', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password', message="Password Mismatched!")])
    agree_to = BooleanField('I agree to the <a href="#">terms</a>', validators=[InputRequired()])


class AdminLoginForm(Form):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])


class AddNewSeason(Form):
    location_from = SelectField('From',default='', validators=[DataRequired()])
    location_to = SelectField('To',default='', validators=[DataRequired()])
    season_class = SelectField('Class', validators=[DataRequired()])