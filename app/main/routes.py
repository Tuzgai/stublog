from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_required
from datetime import datetime

from app import db
from app.main import bp
from app.models import User, Post
from app.main.forms import SubmitPostForm

@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@bp.route('/submit_post', methods=['GET', 'POST'])
@login_required
def submitPost():
    form = SubmitPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user, timestamp=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!', 'success')
        return redirect(url_for('main.index'))
    return render_template('submit_post.html', title="Submit Post", form=form)

@bp.route('/post/<post>')
def viewPost(post):
    post = Post.query.filter_by(id=post).first()
    return render_template('post.html', title=post.title, post=post)

@bp.route('/post/<post>/edit', methods=['GET', 'POST'])
@login_required
def editPost(post):
    post = Post.query.filter_by(id=post).first()
    if post is None or current_user.username is not post.author.username:
        flash('You cannot edit posts you did not create.', 'danger')
        return redirect(url_for('main.index'))
    form = SubmitPostForm(post=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.last_edited_timestamp = datetime.utcnow()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.viewPost', post=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('edit.html', title='Edit Post', form=form)
    