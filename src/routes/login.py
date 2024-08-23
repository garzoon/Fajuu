from flask import Blueprint, render_template

login_scope = Blueprint("login_scope", __name__)

@login_scope.route('/')
def login():
    return render_template('auth/login.html')