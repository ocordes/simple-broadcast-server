"""

app/main/forms.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-05-29

"""


from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
                    SubmitField, TextAreaField, SelectField, SelectMultipleField, \
                    DateField, DateTimeField, RadioField 
#from wtforms_html5 import AutoAttrMeta

from wtforms.validators import ValidationError, DataRequired, Optional, Email, EqualTo, Length
from app.models import User, severities

from wtforms import widgets, SelectMultipleField

from flask_babel import lazy_gettext as _

import datetime


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddLabelForm(FlaskForm):
    name = StringField(_('Name'), validators=[DataRequired()])
    hint = StringField(_('Description'), validators=[DataRequired()])

    submit = SubmitField(_('Submit'))


class EditLabelForm(FlaskForm):
    name = StringField(_('Name'), validators=[DataRequired()])
    hint = StringField(_('Description'), validators=[DataRequired()])

    submit = SubmitField(_('Update'))


class DeleteLabelForm(FlaskForm):
    remove = SubmitField(_('Delete'))


class AddMessageForm(FlaskForm):
    title = StringField(_('Message title'), validators=[DataRequired()])
    valid = DateTimeField(_('Starting date/time'), format='%Y-%m-%d %H:%M')
    severity = RadioField(
        #'Severity', choices=[(1, 'Information'), (2, 'Feature'), (3,'Problem'), (4, 'Outage')], 
        _('Severity'), choices=[(1, severities[1]), (2, severities[2]), (3, severities[3]), (4, severities[4])], 
        coerce=int, default=1, validators=[DataRequired()])
    label = SelectField(coerce=int)
    send_email = BooleanField(_('Send email to ...'), default=False)
    email_body = TextAreaField(_('Email body'), validators=[Optional(), Length(max=200)])
    submit = SubmitField(_('Submit'))


    def validate_valid(self, valid):
        if valid.data is None:
            raise ValidationError(_('Date/Time is not in this format: YYYY-MM-DD HH:MM'))
        
        timediff = (valid.data - datetime.datetime.now()).total_seconds()
        if timediff <= 0:
            raise ValidationError(_('Date/Time must be in the future!'))



class EditMessageForm(FlaskForm):
    title = StringField(_('Message title'), validators=[DataRequired()])
    valid = DateTimeField(_('Starting date/time'), format='%Y-%m-%d %H:%M')
    severity = RadioField(
        #'Severity', choices=[(1, 'Information'), (2, 'Feature'), (3,'Problem'), (4, 'Outage')], 
        _('Severity'), choices=[(1, severities[1]), (2, severities[2]), (3, severities[3]), (4, severities[4])], 
        coerce=int, default=1, validators=[DataRequired()])
    label = SelectField(coerce=int)
    send_email = BooleanField(_('Send email to ...'), default=False)
    email_body = TextAreaField(_('Email body'), validators=[Optional(), Length(max=200)])
    submit = SubmitField(_('Update'))


    def validate_valid(self, valid):
        if valid.data is None:
            raise ValidationError(_('Date/Time is not in this format: YYYY-MM-DD HH:MM'))
        
        timediff = (valid.data - datetime.datetime.now()).total_seconds()
        if timediff <= 0:
            raise ValidationError(_('Date/Time must be in the future!'))



class DeleteMessageForm(FlaskForm):
    remove = SubmitField(_('Delete'))


# ------------------------------------------------------------
#
# email part

# helper class to mimik individual data fields
class _Emailfield(object):
    def __init__(self, data,gettext):
        self.data = data
        self.gettext = gettext


# wrapper around the email normal validator
class MultipleEmails(object):
    def __init__(self, delimiter=','):
        self._delimiter = delimiter


    def __call__(self, form, field):
        email_validator = Email()

        emails = field.data.split(self._delimiter)
        for email in emails:
            email_validator(form, _Emailfield(email,field.gettext))
    


class AddEmailForm(FlaskForm):
    name = StringField(_('Name of email group'), validators=[DataRequired()])
    email = StringField(_('Email address'), validators=[DataRequired(), MultipleEmails()])

    submit = SubmitField(_('Submit'))


class EditEmailForm(FlaskForm):
    name = StringField(_('Name of email group'), validators=[DataRequired()])
    email = StringField(_('Email address'), validators=[DataRequired(), MultipleEmails()])

    submit = SubmitField(_('Update'))


class DeleteEmailForm(FlaskForm):
    remove = SubmitField(_('Delete'))