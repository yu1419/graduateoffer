from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     SelectMultipleField, IntegerField, BooleanField,
                     PasswordField, RadioField, FloatField)
from wtforms.validators import Required, Optional, Email, Length


class Filter(FlaskForm):
    result = SelectField(u'Result', choices=[('', 'All'), ('Offer', 'Offer'),
                         ('AD', 'AD'), ('Rejection', 'Rejection'),
                         ('Wait list', 'Wait list')], id="result")
    degree = SelectField(u'Degree', choices=[('', 'All'),
                         ('Master', 'Master'),
                         ('PhD', 'PhD'), ('JD/LLM', 'JD/LLM')], id="degree")
    min_rank = IntegerField("Univ Rank:", default=1, id="min_rank")
    max_rank = IntegerField("-", default=78, id="max_rank")

    filter_gpa = BooleanField('Filter GPA', default=False, id="filter_gpa")
    min_gpa = FloatField("GPA:", default=2.0, id="min_gpa")
    max_gpa = FloatField("-", default=100, id="max_gpa")

    filter_toefl = BooleanField('Filter TOEFL', default=False,
                                id="filter_toefl")
    min_toefl = IntegerField("TOEFL:", default=70, id="min_toefl")
    max_toefl = IntegerField("-", default=120, id="max_toefl")

    college_type = SelectField(u'College',
                               choices=[('', 'All'), ('985', '985'),
                                        ('211', '211'), ('Abroad', 'Abroad')],
                               default="",
                               id="college")
    major = SelectField(u'Major', id="major")
    sort = SelectField(u'Sorted by',
                       choices=[('received_date', 'Received Date'),
                                ('rank', 'Rank'),
                                ('gpa', 'GPA'), ('toefl', 'TOEFL')], id="sort")

    submit = SubmitField('Search', id="SubmitButton")


class Post_form(FlaskForm):
    content = StringField('Sugguestions or Questions:', validators=[Required()])
    submit = SubmitField('Submit')


class Comment_form(FlaskForm):
    content = StringField('Reply:', validators=[Required()])
    submit = SubmitField('Submit')



class Login_form(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class Register_form(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password',
                             validators=[Required(), Length(6, 64)])
    submit = SubmitField('Register')


class Update_passowrd(FlaskForm):
    old_pass = PasswordField('Old Password',
                             validators=[Required(), Length(6, 64)])
    new_pass = PasswordField('New Password',
                             validators=[Required(), Length(6, 64)])
    submit = SubmitField('Reset')


class Send_email(FlaskForm):
    email = StringField('Please enter your email',
                        validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Send Email')
