from flask import render_template, redirect, url_for, session
from flask_jwt_extended import jwt_required
from . import main_bp
from main.services import get_identity

@main_bp.route('/')
def index():
    if 'access_token' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@jwt_required()
def dashboard():
    user, role = get_identity()
    if user:
        return render_template('dashboard.html',user=user, role=role)
        
    return redirect(url_for('auth.login'))