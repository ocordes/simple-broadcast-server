"""

app/auth/users.py

written by: Oliver Cordes 2022-03-29
changed by: Oliver Cordes 2022-03-29

"""


from flask import current_app, request, render_template, \
                  url_for, flash, redirect
from flask_login import current_user, login_required

from sqlalchemy import desc

from app import db
from app.auth import bp
from app.models import User

from app.auth.forms import UserListForm,  \
                            NewUserForm, EditUserForm



from app.auth.admin import admin_required



@bp.route('/users', methods=['GET','POST'])
@login_required
@admin_required
def users():
    form = UserListForm()
    if form.validate_on_submit():
        # get a list of selected items
        selected_users = request.form.getlist("users")

        for uid in selected_users:
            # skip admin account
            if uid == '1':
                continue
            user = User.query.get(int(uid))
            # sets admin role
            if form.set_admin.data:
                if not user.administrator:
                    msg = 'set admin for user={} ({})'.format(uid,user.username)
                    current_app.logger.info(msg)
                    user.administrator = True
                    flash(msg)
            # clear admin role
            elif form.clear_admin.data:
                if user.administrator:
                    msg = 'clear admin for user={} ({})'.format(uid,user.username)
                    current_app.logger.info(msg)
                    user.administrator = False
                    flash(msg)
            # remove account
            elif form.remove.data:
                db.session.delete(user)
                msg = 'remove account user={} ({})'.format(uid,user.username)
                current_app.logger.info(msg)
                flash(msg)

        db.session.commit()
    return render_template('auth/users.html',
                            title='Users',
                            users=User.query.all(), form=form)


@bp.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
    if not current_user.administrator:
        if username != current_user.username:
            flash('You are not allowed to change other users!')
            return redirect(url_for('main.index'))
    user = User.query.filter_by(username=username).first_or_404()

    # setup the form
    form = EditUserForm()

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data

        # change password only if a new password is set!
        if form.password.data != '':
            user.set_password(form.password.data)

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.user', username=user.username))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.password.data = ''
        form.password2.data = ''
    else:
        print('hugo')
        print(form.password.data)


    return render_template('auth/edituser.html',
                            title='User preferences',
                            user=user,
                            nform=form )



@bp.route('/newuser', methods=['GET','POST'])
@login_required
@admin_required
def newuser():
    nform = NewUserForm()
    if nform.validate_on_submit():
        user = User(username=nform.username.data)
        user.set_password(nform.password.data)
        user.first_name = nform.first_name.data
        user.last_name = nform.last_name.data
        user.email = nform.email.data
        user.is_active = True


        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.users'))

    return render_template('auth/newuser.html',
                            title='New User',
                            nform=nform)
