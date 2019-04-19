from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Blogs(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100))
    body= db.Column(db.String(1000))
    author_name= db.Column(db.String(100))
    created_at= db.Column(db.DateTime(),server_default=db.func.now())
    updated_at= db.Column(db.DateTime(),server_default=db.func.now(), server_onupdate=db.func.now())

db.create_all()


@app.route("/")
def hello():
    return "Hello world"

@app.route("/blog")
def blog():
    test = Blogs.query.all()
    return render_template('blog.html', test=Blogs)