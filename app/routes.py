from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from app.get_data import Post, db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for user {}, remember_me {}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/create', methods=['POST', 'GET'])
def create_post():
    error = None
    if request.method == 'POST':
        try:
            get_post()
        except Exception as e:
            print("Error is", e, "type of e", type(e))
        return redirect(url_for('posts'))
    else:
        return render_template("create.html", title="Create Post")


def get_post():
    post = Post(
        title=request.form['title'],
        body=request.form['body'],
        author_name=request.form['author_name']
    )
    db.session.add(post)
    db.session.commit()
    db.create_all()

@app.route('/blog')
def posts():
    p = Post.query.all()
    return render_template("blog.html", posts=p)
