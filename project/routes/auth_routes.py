from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_connection

from middleware.auth import is_valid_session
import hashlib
from utils.logger import log_action, log_failed_access, log_authentication

auth_routes = Blueprint('auth', __name__)  # Ensure the blueprint name is 'auth'

def hash_password_md5(password):
    # Encode the password to bytes, then create MD5 hash
    md5_hash = hashlib.md5(password.encode())
    return md5_hash.hexdigest()

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        unhashed_password = request.form['password']
        password = hash_password_md5(unhashed_password)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT members.ID AS id, members.emailID AS email, Login.Role AS Role 
            FROM members 
            INNER JOIN Login ON members.ID = Login.MemberID 
            WHERE members.emailID = %s AND Login.Password = %s
        """, (email, password))
        
        user = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are consumed to avoid unread result error
        cursor.close()
        conn.close()
        ip_address = request.remote_addr
        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['Role'] 
            log_authentication(member_id=user['id'], ip_address=ip_address, status='Success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            log_authentication(member_id=None, ip_address=ip_address, status='Failed')
            log_failed_access(member_id=None, document_id=None, reason='Invalid login credentials')
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        unhashed_password = request.form['password']
        password = hash_password_md5(unhashed_password)
        role = 'User'
        conn = get_connection(1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (UserName, emailID) VALUES (%s, %s)", (name, email))
        print("inserted in members")
        member_id = cursor.lastrowid
        cursor.execute("INSERT INTO Login (MemberID, Password, Role) VALUES (%s, %s, %s)", (member_id, password, role))
        
        conn2 = get_connection(0)
        cursor2 = conn2.cursor()
        cursor2.execute("INSERT INTO member (MemberID, Name, Email, ContactNumber, PasswordHash, Role) VALUES (%s, %s, %s, %s, %s, %s)", (member_id, name, email, "0000000000", password, role))
        print("inserted in members")
        
        conn.commit()
        cursor.close()
        conn.close()
        conn2.commit()
        cursor2.close()
        conn2.close()
        log_action(member_id=member_id, action_type='Register', action_details='User registered successfully')
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_routes.route('/create_admin', methods=['GET', 'POST'])
@is_valid_session
def create_admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied. Only admins can create new admins.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        unhashed_password = request.form['password']
        password = hash_password_md5(unhashed_password)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (UserName, emailID) VALUES (%s, %s)", (name, email))
        member_id = cursor.lastrowid
        cursor.execute("INSERT INTO Login (MemberID, Password, Role) VALUES (%s, %s, %s)", (member_id, password, 'admin'))

        conn2 = get_connection(0)
        cursor2 = conn2.cursor()
        cursor2.execute("INSERT INTO member (MemberID, Name, Email, ContactNumber, PasswordHash, Role) VALUES (%s, %s, %s, %s, %s, %s)", (member_id, name, email, "0000000000", password, "admin"))
        print("inserted in members")
        conn.commit()
        cursor.close()
        conn.close()
        conn2.commit()
        cursor2.close()
        conn2.close()

        log_action(member_id=session['user_id'], action_type='CreateAdmin', action_details=f'Admin created: {name} ({email})')
        flash('New admin created successfully.')
        return redirect(url_for('auth.create_admin'))

    return render_template('create_admin.html')

@auth_routes.route('/logout')
def logout():
    log_action(
            member_id=session['user_id'],
            action_type='Logout',
            action_details='User logged out successfully'
        )
    session.clear()
    return redirect(url_for('auth.login'))
