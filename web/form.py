from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, IntegerField, BooleanField, PasswordField, RadioField
from wtforms.validators import Required, Optional, Email, Length


class Filter(FlaskForm):
    result  = SelectField(u'Result', choices=[('All','All'), ('Offer', 'Offer'),
                          ('AD', 'AD'), ('Rejection', 'Rejection'),
                          ('Wait_list', 'Wait_list'),
                          ('Other', 'Other')], id="result")
    degree  = SelectField(u'Degree', choices=[('All','All'), ('Master', 'Master'),
                          ('PhD', 'PhD'), ('JD/LLM', 'JD/LLM')], id="degree")
    start = IntegerField("Ranking:", default=1, id="start")
    stop = IntegerField("-", default=78, id="stop")

    under_cater = SelectField(u'Applicant Undergraduate School',
                              choices=[('All', 'All'), ('985', '985'),
                                       ('211', '211'), ('Abroad', 'Abroad'),
                                       ('other', 'other')], id="under")
    major = SelectField(u'Major', id="major")
    count_per_page = SelectField(u'Count per page',
                                 choices=[('10', '10'), ('20', '20'),
                                          ('30', '30')],
                                 id="count")
    sort = SelectField(u'Sorted by',
                       choices=[('received_date','Date'), ('ranking', 'Ranking'),
                                ('gpa', 'GPA'), ('toefl', 'TOEFL'), ('gre', 'GRE'),
                                ('gre_aw', 'GRE AW')], id="sort")
    order = RadioField(choices=[('DESC', 'decrease'), ('ASC', 'increase')],
                       default='DESC')

    submit = SubmitField('Search', id="SubmitButton")


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
