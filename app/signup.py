from flask import render_template, flash, redirect, url_for, request
from app.get_data import Post, db, Users


def create_account(form):
    username = form['username']
    user_email = form['email']
    user_password = form['password']
    user = Users(username=username, email=user_email)
    user.set_password(user_password)
    db.session.add(user)
    db.session.commit()
    if user is not None:
        return user
    return None

