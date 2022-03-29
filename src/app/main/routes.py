# -*- coding: utf-8 -*-
"""

app/main/routes.py
~~~~~~~~~~~~~~~~~~

written by : Oliver Cordes 2021-02-12
changed by : Oliver Cordes 2021-02-24

"""

import os
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import pkg_resources

from flask import current_app, request, render_template, url_for, flash,  \
    redirect, send_from_directory, jsonify, session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse, url_unparse

from flask_paginate import Pagination, get_page_parameter

from app import db
from app.main import bp
from app.models import *
from app.main.forms import AddMessageForm

from app.auth.admin import admin_required


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


"""
before_request will be executed before any page will be
rendered
"""
@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    installed_packages = [(d.project_name, d.version)
                          for d in pkg_resources.working_set][::-1]

    server_users = User.query.count()
    return render_template('index.html',
                            installed_packages=installed_packages,
                            server_users=server_users,
                                title='Dashboard'
                            )


@bp.route('/messages', methods=['GET'])
@login_required
def messages():
    return render_template('main/messages.html',
                            title='Messages'
                           )


@bp.route('/add_message', methods=['GET','POST'])
@login_required
def message_add():
    form = AddMessageForm()

    if form.validate_on_submit():
        return redirect(url_for('main.messages'))

    
    return render_template('main/message_add.html',
                           title='Add message',
                           nform=form,
                           )





