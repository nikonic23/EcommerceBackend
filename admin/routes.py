from flask import render_template
from admin import admin_bp
from utils.decorators import admin_required


@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template("admin_dashboard.html")