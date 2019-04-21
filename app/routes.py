from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from app.get_data import Post, db, Users
from app.signup import create_account
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

LoginMana = LoginManager(app)
LoginMana.login_view = 'login'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # if request.method == 'POST':
    #     user_email = request.form['email']
    #     user_password = request.form['password']
    #     user = User.query.filter_by(email=user_email).first()
    #     if(user is not None and user.check_password(user_password)):
    #         flash('Hi! ' + user.username, 'alert-success')
    #         login_user(user)
    #         next = request.args.get('next')
    #         return redirect(next or url_for('profile'))
    #     else:
    #         flash('Wrong Email/Password', 'alert-danger')

    # return render_template('login.html', error=error)

    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login request for user {}, remember_me {}'.format(
        #     form.email.data, form.remember_me.data))
        user_email = form.email.data
        print(user_email)
        user_password = form.password.data
        print(user_password)
        user = Users.query.filter_by(email=user_email).first()
        if(user is not None and user.check_password(user_password)):
            flash('Hi! ' + user.username, 'alert-success')
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('index'))
        else:
            flash('Wrong Email/Password', 'alert-danger')

        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@LoginMana.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    error = None
    if request.method == 'POST':
        try:
            get_post()
        except Exception as e:
            print("Error is", e, "type of e", type(e))
        return redirect(url_for('posts'))
    else:
        return render_template("create.html", title="Create a new post")


def get_post():
    print(request.form['title'])
    post = Post(
        title=request.form['title'],
        body=request.form['body'],
        author_name=request.form['author_name']
    )
    db.session.add(post)
    db.session.commit()


@app.route('/blog')
def posts():
    p = Post.query.all()
    return render_template("blog.html", title="Post Blog Content", posts=p)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout success', 'alert-success')
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def signup_account():
    error = None
    if request.method == 'POST':
        user = create_account(request.form)
        if user is not None:
            return redirect(url_for('create_post'))
    return render_template('signup.html', error=error)
