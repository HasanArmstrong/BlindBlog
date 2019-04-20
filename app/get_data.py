from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/*4920'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())