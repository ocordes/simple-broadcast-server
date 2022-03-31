"""

app/models.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-03-31

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



severity_info    = 0   # green
severity_feature = 1   # blue
severity_problem = 2   # yellow
severity_outage  = 3   # red



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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
