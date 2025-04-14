from flask import Blueprint, render_template, session, redirect, url_for, flash
from middleware.auth import is_valid_session

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.route('/dashboard', methods=['GET'])
@is_valid_session
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to access the dashboard.')
        return redirect(url_for('auth.login'))

    return render_template('index.html')