from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app import bcrypt


@app.route('/')
def index():
    return redirect('/user/login')


@app.route('/user/login')
def login_page():
    return render_template('login_page.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/user/login')


@app.route('/register', methods=['POST'])
def register_user():
    if not User.validate_user_registration(request.form):
        return redirect('/')

    user_id = User.save_user(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email / Password", 'login')
        return redirect('/user/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email / Password", 'login')
        return redirect('/user/login')
    session['user_id'] = user.id

    return redirect('/dashboard')
