"""

app/auth/forms.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-05-29

"""

"""
chromium autocomplete:

https://developers.google.com/web/updates/2015/06/checkout-faster-with-autofill

"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
                    SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.widgets import PasswordInput
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

from wtforms import widgets, SelectMultipleField

from flask_babel import lazy_gettext as _


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()], render_kw={"autocomplete": "current-password"},
)
    remember_me = BooleanField(_('Remember me'))
    submit = SubmitField(_('Login'))



class NewUserForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    first_name = StringField(_('First name'), validators=[DataRequired()])
    last_name = StringField(_('Last name'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Repeated password'), validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField(_('Submit'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class EditUserForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Email()], render_kw={"autocomplete": "email"})
    first_name = StringField(_('First name'), validators=[DataRequired()])
    last_name = StringField(_('Last name'), validators=[DataRequired()])
    password = StringField(_('New password'), widget=PasswordInput(hide_value=False), validators=[], render_kw={"autocomplete": "new-password"},)
    password2 = StringField(_('Repeated password'), widget=PasswordInput(hide_value=False), validators=[EqualTo('password')])
    submit = SubmitField(_('Update'))



class UpdatePasswordForm(FlaskForm):
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Repeated password'), validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField(_('Update Password'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_('Request password reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Repeated password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_('Reset password'))


class AdminPasswordForm(FlaskForm):
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Repeated password'), validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField(_('Set admin password'))


class UserListForm(FlaskForm):
    set_admin = SubmitField(_('Set Admin'))
    clear_admin = SubmitField(_('Clear Admin'))
    remove = SubmitField(_('Remove'))



class PreferencesForm(FlaskForm):
    test_email = StringField(_('Send Email to:'), validators=[DataRequired(), Email()])
    send_email = SubmitField(_('Send Test Email'))
