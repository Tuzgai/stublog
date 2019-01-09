from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_required

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
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!', 'success')
        return redirect(url_for('main.index'))
    return render_template('submit_post.html', title="Submit Post", form=form)

@bp.route('/post/<post>')
def viewPost(post):
    post = Post.query.filter_by(id=post).first()
    return render_template('post.html', post=post)