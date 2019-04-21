from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(10), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(
            password, method='pbkdf2:sha1', salt_length=8)


def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author


db.create_all()


@app.route("/")
def hello():
    return "Hello! Welcome to my page!"


@app.route('/posts')
def posts():
    p = Post.query.all()
    return render_template('posts.html', posts=p)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content'] or not request.form['author']:
            print('Please enter all the fields', 'error')
        else:
            p = Post(request.form['title'], request.form['content'],
                     request.form['author'])

            db.session.add(p)
            db.session.commit()

            print('Post was successfully added')
            return redirect(url_for('posts'))

           # access the data using request.form['field_name']
           # save it to the database
           # return a redirect to /posts
           # the code below is executed if the request method
           # was GET or the credentials were invalid
    return render_template('create.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            print('Please enter all the fields', 'error')
        else:
            l = Profile(
                request.form['username'], request.form['email'], request.form['password'])

            db.session.add(l)
            db.session.commit()

            print('Signed up')
        return redirect(url_for('profiles'))
    return render_template('login.html', next=next)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            print('Please enter all the fields', 'error')
        else:
            l = Profile(
                request.form['username'], request.form['email'], request.form['password'])

            db.session.add(l)
            db.session.commit()

            print('Logged in')
        return redirect(url_for('create'))
    return render_template('login.html', next=next)
