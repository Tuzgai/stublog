from flask import render_template, flash, redirect

from app import db
from app.main import bp
from app.models import User, Post
from app.main.forms import SubmitPostForm

@bp.route('/')
@bp.route('/index.html')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@bp.route('/submit_post.html', methods=['GET', 'POST'])
def submitPost():
    form = SubmitPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=User.query.filter_by(username=form.author.data).first())
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!', 'Success')
        return redirect('index.html')
    return render_template('submit_post.html', form=form)