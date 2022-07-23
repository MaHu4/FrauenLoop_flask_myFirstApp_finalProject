from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField, TextAreaField
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
    lookup_address = StringField('Search address')
    coord_latitude = HiddenField('Latitude',validators=[DataRequired()])
    coord_longitude = HiddenField('Longitude', validators=[DataRequired()]) 

    location_name = StringField('Name of the location', validators=[DataRequired(), Length(min=1, max=50)])
    shop_category = SelectField(u'Select shop category', choices=[('1','Secondhand store / boutique'),('2', 'Fairfashion store'),('3','Rental store for clothes'), ('4','Designer fashion store'),('5','Swap box / cupboard'),('6','Flea market for clothes'),('7','Tailor or shoe maker / repairer'),('8', 'Upcycling'),('9','Clothes donations'),('10','Eco laundry')])     
    description = TextAreaField('Location description', validators=[DataRequired(), Length(min=1, max=500)])                

    submit = SubmitField('Create Location')
