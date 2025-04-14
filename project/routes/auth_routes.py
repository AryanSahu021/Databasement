from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_connection
from middleware.auth import is_valid_session

auth_routes = Blueprint('auth', __name__)  # Ensure the blueprint name is 'auth'

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # cursor.execute("SELECT * FROM Login WHERE email = %s AND password = %s", (email, password))
        cursor.execute("""
            SELECT members.ID AS id, members.emailID AS email, Login.Role AS Role 
            FROM members 
            INNER JOIN Login ON members.ID = Login.MemberID 
            WHERE members.emailID = %s AND Login.Password = %s
        """, (email, password))
        
        user = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are consumed to avoid unread result error
        cursor.close()
        print("+++++", user)
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['Role'] 
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
        role = 'User'
        conn = get_connection(1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (UserName, emailID) VALUES (%s, %s)", (name, email))
        print("inserted in members")
        member_id = cursor.lastrowid
        cursor.execute("INSERT INTO Login (MemberID, Password, Role) VALUES (%s, %s, %s)", (member_id, password, role))
        conn.commit()
        cursor.close()
        conn.close()
        
        conn = get_connection(0)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member (MemberID, Name, Email, ContactNumber, PasswordHash, Role) VALUES (%s, %s, %s, %s, %s, %s)", (member_id, name, email, "0000000000", password, role))
        print("inserted in members")
        conn.commit()
        cursor.close()
        conn.close()

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
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (UserName, emailID) VALUES (%s, %s)", (name, email))
        member_id = cursor.lastrowid
        cursor.execute("INSERT INTO Login (MemberID, Password, Role) VALUES (%s, %s, %s)", (member_id, password, 'admin'))
        conn.commit()
        cursor.close()
        conn.close()

        conn = get_connection(0)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member (MemberID, Name, Email, ContactNumber, PasswordHash, Role) VALUES (%s, %s, %s, %s, %s, %s)", (member_id, name, email, "0000000000", password, "admin"))
        print("inserted in members")
        conn.commit()
        cursor.close()
        conn.close()

        flash('New admin created successfully.')
        return redirect(url_for('auth.create_admin'))

    return render_template('create_admin.html')



from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from db import get_connection
import os

file_routes = Blueprint('files', __name__)

@file_routes.route('/files', methods=['GET'])
def list_files():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)

    # Fetch files the user has access to
    cursor.execute("""
        SELECT d.DocumentID, d.FilePath, a.AccessLevel
        FROM pdfdocument d
        JOIN accesscontrol a ON d.DocumentID = a.DocumentID
        WHERE a.MemberID = %s
    """, (user_id,))
    files = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('files.html', files=files)

@file_routes.route('/files/<int:document_id>', methods=['GET'])
def view_file(document_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)

    # Check if the user has access to the file
    cursor.execute("""
        SELECT d.FilePath, a.AccessLevel
        FROM pdfdocument d
        JOIN accesscontrol a ON d.DocumentID = a.DocumentID
        WHERE a.MemberID = %s AND d.DocumentID = %s
    """, (user_id, document_id))
    access = cursor.fetchone()

    cursor.close()
    conn.close()

    if not access:
        flash('You do not have access to this file.')
        return redirect(url_for('files.list_files'))

    # If access level is valid, serve the file
    return redirect(access['FilePath'])

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))




# @auth_routes.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT MemberID AS id, Email AS email, Role
#             FROM member
#             WHERE Email = %s AND PasswordHash = %s
#         """, (email, password))
        
#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if user:
#             session['user_id'] = user['id']
#             session['email'] = user['email']
#             session['role'] = user['Role']
#             return redirect(url_for('files.list_files'))
#         else:
#             flash('Invalid credentials. Please try again.')
#     return render_template('login.html')

# @auth_routes.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         role = 'User'

#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO members (Name, Email, PasswordHash, Role)
#             VALUES (%s, %s, %s, %s)
#         """, (name, email, password, role))
#         conn.commit()
#         cursor.close()
#         conn.close()

#         flash('Registration successful. Please log in.')
#         return redirect(url_for('auth.login'))
#     return render_template('register.html')