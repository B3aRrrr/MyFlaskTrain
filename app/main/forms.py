from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,BooleanField,SelectField
from wtforms import ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Length(1,64),Email()])
    username = StringField('Username',validators=[InputRequired(),Length(1,64),Regexp(
        '^[A-Za-z] [A-Za-z0-9_.]*$',0,
        'Usernames must have only letters' 'numbers, dots or underscores'
    )])
    confirmed = BooleanField("Confirmed")
    role = SelectField('Role',coerce=int)
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(1,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [
            (role.id,role.name) for role in Role.query.order_by(Role.name).all()
        ]
        self.user = user
    
    def validate_email(self,field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_username(self, field):
        if field.data != self.user.username and \
            User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')