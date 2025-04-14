from flask import Blueprint, render_template, session, redirect, url_for
from db import get_connection

file_routes = Blueprint('files', __name__)

@file_routes.route('/files', methods=['GET'])
def list_files():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.id, d.filename, d.file_path
        FROM documents d
        JOIN document_access a ON d.id = a.document_id
        WHERE a.user_id = %s
    """, (user_id,))
    files = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('files.html', files=files)