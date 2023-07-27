from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask import Flask
from flask_bcrypt import Bcrypt

@app.route('/')
def index():
    return redirect('/user/login')

@app.route('/user/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('login.html') #template name needed

@app.route('/user/login/process', methods=['POST'])
def login_success():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not Bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    session['name'] = user.first_name
    return redirect('/dashboard')

@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not User.validate_reg(request.form):
        return redirect('/user/login')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": Bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/user/login')