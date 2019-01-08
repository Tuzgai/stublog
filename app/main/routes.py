from flask import render_template, flash

from app.main import bp
from app.models import User, Post

@bp.route('/')
@bp.route('/index.html')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)