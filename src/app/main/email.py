# -*- coding: utf-8 -*-
"""

app/main/email.py
~~~~~~~~~~~~~~~~~~

written by : Oliver Cordes 2022-05-13
changed by : Oliver Cordes 2022-05-13

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
from app.main.forms import AddEmailForm, EditEmailForm, DeleteEmailForm


from app.auth.admin import admin_required


@bp.route('/emails', methods=['GET', 'POST'])
@login_required
def show_emails():
    dform = DeleteEmailForm()

    if dform.validate_on_submit():
        selected_labels = request.form.getlist("remove_group")

        for id in selected_labels:
            email_address = EmailAddress.query.get(int(id))
            db.session.delete(email_address)
            db.session.commit()

    email_addresses = EmailAddress.query.all()

    return render_template('main/emails.html',
                            email_addresses=email_addresses,
                            dform=dform,
                            title='Email groups'
    )


@bp.route('/email/add', methods=['GET', 'POST'])
@login_required
def email_add():
    form = AddEmailForm()

    if form.validate_on_submit():
        email_address = EmailAddress(name=form.name.data, emails=form.email.data)
        db.session.add(email_address)
        db.session.commit()

        return redirect(url_for('main.show_emails'))

    return render_template('main/email_edit.html',
                           title='New email group',
                           edit=False,
                           nform=form,
                           )


@bp.route('/email/<id>/edit', methods=['GET', 'POST'])
@login_required
def email_edit(id):

    form = EditEmailForm()

    email_address = EmailAddress.query.get(int(id)) 

    if form.validate_on_submit():
        email_address.name = form.name.data
        email_address.emails = form.email.data
        db.session.commit()

        return redirect(url_for('main.show_emails'))
    elif request.method == 'GET':
        form.name.data = email_address.name
        form.email.data = email_address.emails

    return render_template('main/email_edit.html',
                            title='Edit an email group',
                            edit=True,
                            nform=form
                            )


@bp.route('/email/<id>/delete')
@login_required
def email_delete(id):
    email_address = EmailAddress.query.get(int(id)) 
    db.session.delete(email_address)
    db.session.commit()

    return redirect(url_for('main.show_emails'))