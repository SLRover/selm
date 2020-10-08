from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Regexp
import pytz

all_timezones = [(tz, tz) for tz in pytz.all_timezones]
date_regex = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))' \
             r'(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|' \
             r'[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|' \
             r'(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'


class SetupForm(FlaskForm):
    database = SelectField(label='Database type', choices=[('sqlite', 'SQLite'), ('postgresql', 'PostgreSQL')])
    url = StringField(label='DB URL')
    user = StringField(label='DB User')
    password = StringField(label='DB Password')
    name = StringField(label='DB Name')
    port = StringField(label='DB Port')
    tz = SelectField(label='Timezone', choices=all_timezones)
    submit = SubmitField(label='Setup')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField(label='Login')


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = StringField(label='E-mail', validators=[DataRequired()])
    full_name = StringField(label='Full name')
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Register')


class AddLicenseForm(FlaskForm):
    product = StringField(label='Product', validators=[DataRequired()])
    key = StringField(label='Key', validators=[DataRequired()])
    expire = StringField(label='Expire', validators=[Optional(), Regexp(date_regex, message='Error')])
    email = StringField(label='E-mail', validators=[Optional()])
    active = BooleanField(label='Active')
    submit = SubmitField(label='Add license')


class EditLicenseForm(FlaskForm):
    id = StringField(validators=[DataRequired()])
    product = StringField(label='Product', validators=[DataRequired()])
    key = StringField(label='Key', validators=[DataRequired()])
    expire = StringField(label='Expire', validators=[Optional()])
    email = StringField(label='E-mail', validators=[Optional()])
    active = BooleanField(label='Active')
    submit = SubmitField(label='Update License')


class RemoveLicenseForm(FlaskForm):
    remove_id = StringField(validators=[DataRequired()])
    remove_submit = SubmitField(label='Confirm')
