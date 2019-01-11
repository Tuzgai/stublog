from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app import db
from app.profile import bp
from app.models import User, Post
from app.profile.forms import EditProfileForm

@bp.route('/profile/<username>')
def profile(username):
    if username == '[removed]':
        flash('The requested profile could not be found.', 'warning')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('The requested profile could not be found.', 'warning')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('profile.profile', username=username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('profile.profile', username=username, page=posts.prev_num) if posts.has_prev else None
    return render_template('profile/profile.html', title='Profile', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
    
@bp.route('/profile/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None or user.username is not current_user.username:
        flash("You cannot edit another person's profile.", 'danger')
        return redirect('main.index')
    form = EditProfileForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved!', 'success')
        return redirect(url_for('profile.profile', username=username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.bio.data = user.bio
    return render_template('profile/edit_Profile.html', title='Edit Profile', form=form, user=user)