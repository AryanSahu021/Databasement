from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_connection

auth_routes = Blueprint('auth', __name__)  # Ensure the blueprint name is 'auth'

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('files.list_files'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
        member_id = cursor.lastrowid
        cursor.execute("INSERT INTO login (id, email, password) VALUES (%s, %s, %s)", (member_id, email, password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))