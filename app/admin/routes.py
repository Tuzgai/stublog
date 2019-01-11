from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import email

from app import db
from app.admin import bp
from app.models import User, Post
from app.admin.forms import InviteUserForm

import secrets

@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.admin_level < current_app.config['ADMIN_LEVEL_EDIT_USER']:
        flash('You are not authorized to view the admin panel.', 'danger')
        return redirect(url_for('index.main'))
    form = InviteUserForm()
    if form.validate_on_submit():
        password = secrets.token_hex(nbytes=16)
        user = User(email=form.email.data)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        email.send_registration_invitation_email(user)
        flash('Invitation sent!', 'success')
        return redirect(url_for('main.index'))
    users = User.query.order_by(User.id).all()
    return render_template('admin/admin.html', title='Admin', form=form, users=users)

@bp.route('/admin/remove_user')
@bp.route('/admin/remove_user/<username>')
@login_required
def remove_user(username=None):
    if current_user.admin_level < current_app.config['ADMIN_LEVEL_EDIT_USER']:
        flash('You are not authorized to view the admin panel.', 'danger')
        return redirect(url_for('index.main'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User does not exist.', 'danger')
        return redirect(url_for('admin.admin'))
    # I don't want to do anything too destructive to the DB
    # We'll just strike the name and scramble the password
    user.username = '[removed]'
    user.bio = '[removed]'
    user.set_password(secrets.token_hex(nbytes=16))
    db.session.commit()
    return redirect(url_for('admin.admin'))