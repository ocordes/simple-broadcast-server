"""

app/models.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-05-17

"""

import os
import uuid

from app import db, login


from flask import current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from hashlib import md5
from datetime import datetime, timedelta
from time import time
import jwt



severity_info    = 1   # green
severity_feature = 2   # blue
severity_problem = 3   # yellow
severity_outage  = 4   # red


severities = {
            0 : 'Unknown',
            1 : 'Information',
            2 : 'Update',
            3 : 'Problem',
            4 : 'Outage',
}

sev_colors = {
            0 : '#ffffff',
            1 : '#99ff99',
            2 : '#afffff',
            3 : '#eaffaf',
            4 : '#ff9999'
}



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # some internal and private fields
    is_active = db.Column(db.Boolean, default=False)
    administrator  = db.Column(db.Boolean, default=False)

    # Relationships
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


    def get_email_verify_token(self, expires_in=600):
        return jwt.encode(
            {'email_verify': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_email_verify_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['email_verify']
        except:
            return
        return User.query.get(id)


    def __repr__(self):
        return '<User {}>'.format(self.username)


class EmailAddress(db.Model):
    __tablename__ = 'emailaddress'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    emails = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



class MessageLabel(db.Model):
    __tablename__ = 'msglabels'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    hint = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200))
    valid = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.Integer(), default=severity_info)
    label = db.Column(db.Integer(), db.ForeignKey('msglabels.id', ondelete='CASCADE'))
    send_email = db.Column(db.Boolean(), default=False)
    email_body = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def get_severity_name(self):
        return severities[self.severity]

    def get_sev_color(self):
        return sev_colors[self.severity]

    def get_days(self):
        delta = (self.valid-datetime.now()).total_seconds()

        sign = delta < 0 and '-' or ''

        delta = abs(delta)
        days, delta = divmod(delta,86400)
        hours, delta = divmod(delta, 3600)
        mins, seconds = divmod(delta, 60)

        return f'{sign}{int(days)} days, {int(hours):02d}:{int(mins):02d}:{int(seconds):02d} hours'

    def get_days_color(self):
        delta = (self.valid-datetime.now()).total_seconds()

        if delta < 0:
            return 'red'

        if delta < 86400:
            return '#fab778'

        if delta < 86400*7:
            return '#eaffaf'

        return 'white'


    def get_label_name(self):
        label = MessageLabel.query.get(self.label)

        return label.name