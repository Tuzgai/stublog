from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user, login_required
from datetime import datetime

from app import db
from app.main import bp
from app.models import User, Post
from app.main.forms import SubmitPostForm

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None 
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/submit_post', methods=['GET', 'POST'])
@login_required
def submit_post():
    form = SubmitPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user, timestamp=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!', 'success')
        return redirect(url_for('main.index'))
    return render_template('submit_post.html', title="Submit Post", form=form)

@bp.route('/post/<post>')
def view_post(post):
    post = Post.query.filter_by(id=post).first()
    return render_template('post.html', title=post.title, post=post)

@bp.route('/post/<post>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post):
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
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.view_post', post=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('edit.html', title='Edit Post', form=form, post=post)

@bp.route('/post/<post>/delete')
@login_required
def delete_post(post, confirm=False):
    post = Post.query.filter_by(id=post).first()
    confirm = request.args.get('confirm')
    if post is None or current_user.username is not post.author.username:
        flash('You cannot edit posts you did not create.', 'danger')
    elif confirm == 'True':
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted.', 'success')
    return redirect(url_for('main.index'))
    