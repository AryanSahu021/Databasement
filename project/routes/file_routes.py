from flask import Blueprint, render_template, session, redirect, url_for
from db import get_connection

file_routes = Blueprint('files', __name__)

@file_routes.route('/files', methods=['GET'])
def list_files():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.DocumentID, d.FilePath, d.UploadTimestamp, a.AccessLevel
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
    cursor.execute("""
        SELECT a.AccessLevel, d.FilePath
        FROM accesscontrol a
        JOIN pdfdocument d ON a.DocumentID = d.DocumentID
        WHERE a.MemberID = %s AND a.DocumentID = %s
    """, (user_id, document_id))
    access = cursor.fetchone()
    cursor.close()
    conn.close()

    if not access:
        flash('You do not have access to this document.')
        return redirect(url_for('files.list_files'))

    # Log the access attempt
    log_action(user_id, 'View', 'Viewed document', document_id)

    # Open the file in a new window
    return redirect(access['FilePath'])