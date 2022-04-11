"""

app/main/forms.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-04-11

"""


from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
                    SubmitField, TextAreaField, SelectField, SelectMultipleField, \
                    DateField, DateTimeField, RadioField 
#from wtforms_html5 import AutoAttrMeta

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, severities

from wtforms import widgets, SelectMultipleField

import datetime


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class AddUserForm(FlaskForm):
    group = SelectField(coerce=int)
    users = TextAreaField(u'User IDs')
    submit = SubmitField('Add')
    
class DeleteWhitelistUserForm(FlaskForm):
    group = SelectField(coerce=int)
    select = SubmitField('Select')
    remove = SubmitField('Delete')


class AddLabelForm(FlaskForm):
    name = StringField('Name of label', validators=[DataRequired()])
    hint = StringField('Description', validators=[DataRequired()])

    submit = SubmitField('Submit')


class EditLabelForm(FlaskForm):
    name = StringField('Name of label', validators=[DataRequired()])
    hint = StringField('Description', validators=[DataRequired()])

    submit = SubmitField('Update')



class DeleteLabelForm(FlaskForm):
    remove = SubmitField('Delete')


class AddMessageForm(FlaskForm):
    #class Meta(AutoAttrMeta):
    #    pass
    title = StringField('Message title', validators=[DataRequired()])
    valid = DateTimeField('Starting date/time', format='%Y-%m-%d %H:%M')
    severity = RadioField(
        #'Severity', choices=[(1, 'Information'), (2, 'Feature'), (3,'Problem'), (4, 'Outage')], 
        'Severity', choices=[(1, severities[1]), (2, severities[2]), (3, severities[3]), (4, severities[4])], 
        coerce=int, default=1, validators=[DataRequired()])
    label = SelectField(coerce=int)
    submit = SubmitField('Submit')


    def validate_valid(self, valid):
        if valid.data is None:
            raise ValidationError('Date/Time is not in this format: YYYY-MM-DD HH:MM')
        
        timediff = (valid.data - datetime.datetime.now()).total_seconds()
        if timediff <= 0:
            raise ValidationError('Date/Time must be in the future!')


class DeleteMessageForm(FlaskForm):
    remove = SubmitField('Delete')