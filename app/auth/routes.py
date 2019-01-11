from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.auth import bp
from app.models import User, Post
from app.auth.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.email import send_password_reset_email

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_app.config['PUBLIC_REGISTRATION_OPEN']:
        if current_user.is_authenticated:
            flash('You are already logged in!', 'warning')
            return redirect(url_for('main.index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, 
                        email = form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You are now registered!', 'success')
            return redirect(url_for('main.index'))
        return render_template('auth/register.html',
                               title='Register', form=form)
    flash('Public registration is currently closed.', 'warning')
    return redirect(url_for('main.index'))

@bp.route('register/<token>', methods=['GET', 'POST'])
def invited_user(token):
    if current_user.is_authenticated:
        flash('You are already logged in.', 'caution')
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid registration link', 'danger')
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user.username=form.username.data
        user.email=form.email.data
        user.set_password(form.password.data)
        db.session.commit()
        flash('You are now registered!', 'success')
    return render_template('auth/register.html',
                           title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'warning')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    if not current_user.is_authenticated:
        flash('You are already logged out!', 'warning')
        return redirect(url_for('main.index'))
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Instructions for resetting your password have been sent! Please check your email.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@bp.route('reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid password reset link', 'danger')
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)