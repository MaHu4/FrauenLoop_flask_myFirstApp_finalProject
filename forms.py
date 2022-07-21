from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField



## LOGIN FORM

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember me')

    submit = SubmitField('Login')    

## REGISTRATION FORM

class RegistrationForm(FlaskForm):
    fullname = StringField(
        'Full Name', 
        validators=
            [DataRequired(), 
            Length(min=2, max=200)
        ]
    )

    username = StringField(
        'Username', 
        validators=
            [DataRequired(), 
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(), 
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign up')  


## NEW LOCATIION IN MAP

class NewLocationForm(FlaskForm):
    description = StringField('Location description', validators=[DataRequired(), Length(min=1, max=500)])
    lookup_address = StringField('Search address')

    coord_latitude = HiddenField('Latitude',validators=[DataRequired()])

    coord_longitude = HiddenField('Longitude', validators=[DataRequired()]) 
    category = SelectField(u'Category', choices=[('1', 'Secondhand Shop'),('2', 'Fairfashion Shop'),('3','Swap box/cupboard'),('4','Flea market')])                   

    submit = SubmitField('Create Location')
