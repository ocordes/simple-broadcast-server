# -*- coding: utf-8 -*-
"""

app/main/routes.py
~~~~~~~~~~~~~~~~~~

written by : Oliver Cordes 2022-03-29
changed by : Oliver Cordes 2022-04-12

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
from app.main.forms import AddLabelForm, EditLabelForm, DeleteLabelForm, \
        AddMessageForm, EditMessageForm, DeleteMessageForm

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


@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'


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


@bp.route('/labels', methods=['GET', 'POST'])
@login_required
def show_labels():
    dform = DeleteLabelForm()

    if dform.validate_on_submit():
        print('remove pressed')
        selected_labels = request.form.getlist("remove_group")
        print(selected_labels)

        for id in selected_labels:
            label = MessageLabel.query.get(int(id))
            print(label)
            db.session.delete(label)
            db.session.commit()

    labels = MessageLabel.query.all()

    return render_template('main/labels.html',
                            labels=labels,
                            dform=dform,
                            title='Labels'
    )


@bp.route('/label/add', methods=['GET', 'POST'])
@login_required
def label_add():
    form = AddLabelForm()

    if form.validate_on_submit():
        label = MessageLabel(name=form.name.data, hint=form.hint.data)
        db.session.add(label)
        db.session.commit()

        return redirect(url_for('main.show_labels'))

    return render_template('main/label_edit.html',
                           title='Add label',
                           edit=False,
                           nform=form,
                           )


@bp.route('/label/<id>/edit', methods=['GET', 'POST'])
@login_required
def label_edit(id):

    form = EditLabelForm()

    label = MessageLabel.query.get(int(id)) 

    if form.validate_on_submit():
        label.name = form.name.data
        label.hint = form.hint.data
        db.session.commit()

        return redirect(url_for('main.show_labels'))
    elif request.method == 'GET':
        form.name.data = label.name
        form.hint.data = label.hint

    return render_template('main/label_edit.html',
                            title='Edit label',
                            edit=True,
                            nform=form
                            )


@bp.route('/label/<id>/delete')
@login_required
def label_delete(id):
    return redirect(url_for('main.show_labels'))



@bp.route('/messages', methods=['GET', 'POST'])
@login_required
def show_messages():
    # analyse the request
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page     = request.args.get(get_page_parameter(), type=int, default=1)

    print('page:', page)

    dform = DeleteMessageForm()

    if dform.validate_on_submit():
        print('remove pressed')
        # get a list of selected items
        selected_messages = request.form.getlist("remove_group")
        print(selected_messages)

        for id in selected_messages:
            msg = Message.query.get(int(id))
            db.session.delete(msg)
            db.session.commit()

        return redirect(url_for('main.show_messages'))

    max_messages = Message.query.count()

    pagination = Pagination(page=page, total=max_messages,
                            per_page=10,
                            css_framework='bootstrap4',
                            href=url_for('main.show_messages') +
                            '?page={}',
                            display_msg='(Displaying <b>{start}-{end}</b> of <b>{total}</b> Messages)',
                            search=search, record_name='whitelist_users')

    messages = Message.query.order_by(Message.valid).paginate(page, pagination.per_page, error_out=False).items

    return render_template('main/messages.html',
                            title='Messages',
                            dform=dform,
                            pagination=pagination,
                            messages=messages
                           )


@bp.route('/message/add', methods=['GET','POST'])
@login_required
def message_add():
    form = AddMessageForm()

    labels = MessageLabel.query.all()
    form.label.choices = [(l.id, l.name) for l in labels]

    if form.validate_on_submit():

        msg = Message(title=form.title.data)
        msg.valid = form.valid.data
        msg.severity = form.severity.data
        msg.label = form.label.data

        db.session.add(msg)
        db.session.commit()

        return redirect(url_for('main.show_messages'))

    
    return render_template('main/message_edit.html',
                           title='Add message',
                           edit=False,
                           nform=form,
                           )



@bp.route('/message/<id>/edit')
@login_required
def message_edit(id):
    form = EditMessageForm()

    labels = MessageLabel.query.all()
    form.label.choices = [(l.id, l.name) for l in labels]

    msg = Message.query.get(int(id))

    if form.validate_on_submit():

        return redirect(url_for('main.show_messages'))

    form.title.data    = msg.title
    form.valid.data    = msg.valid
    form.severity.data = msg.severity
    form.label.data    = msg.label
    
    return render_template('main/message_edit.html',
                           title='Edit message',
                           edit=True,
                           nform=form,
                           )


@bp.route('/message/<id>/delete')
@login_required
def message_delete(id):
    return redirect(url_for('main.show_messages'))

