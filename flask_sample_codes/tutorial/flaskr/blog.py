from flask import (Blueprint, render_template, request, flash, g, redirect,
                   url_for)

from .db import get_db
from .auth import login_required

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username FROM post p'
        ' JOIN user u ON p.author_id = u.id ORDER BY created DESC').fetchall()
    return render_template('blog/index.html', posts=posts)


@blog_bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('INSERT INTO post (title, body, author_id) VALUES'
                       ' (?, ?, ?)', (title, body, g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))

        return render_template('blog/create.html')
