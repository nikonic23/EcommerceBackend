from flask import render_template, redirect, url_for, session, flash, request
from . import auth_bp
from auth.forms import RegisterForm, LoginForm
from utils.rate_limiter import is_rate_limited
from auth.services import (
    register_user,
    authenticate_user,
    generate_access_token
)


@auth_bp.route('/register', methods=['GET','POST'] )
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        register_user(
            form.name.data,
            form.email.data,
            form.password.data
        )
        return redirect(url_for('auth.login'))

    return render_template('register.html',form = form)


@auth_bp.route('/login', methods=['GET','POST'] )
def login():
    client_ip = request.remote_addr

    if request.method=="POST":
        if is_rate_limited(f"login:{client_ip}", limit=5, window=60):
            flash("Too many login attempts. Try again later.")
            return redirect(url_for("auth.login"))

    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(
            form.email.data,
            form.password.data
        )
        if not user:
            flash("Invalid Credentials")
            return redirect(url_for('auth.login'))

        session['access_token'] = generate_access_token(user)
        session.modified = True
        return redirect(url_for('main.dashboard'))

    return render_template('login.html',form = form)


@auth_bp.route('/api/login',methods=['POST'])
def api_login():
    data = request.json
    user = authenticate_user(
        data.get("email"),
        data.get("password")
    )

    if not user:
        return {"msg": "Invalid Credentials"}, 401
    
    return{
        "access_token": generate_access_token(user)
    }


@auth_bp.route('/logout', methods=['POST'])
def logout():

    session.pop('access_token', None)
    flash("You have been logged out successfully. ")

    return redirect(url_for('auth.login'))