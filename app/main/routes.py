from flask import render_template, flash

from app.main import bp

@bp.route('/')
@bp.route('/index.html')
def index():
    return render_template('index.html')