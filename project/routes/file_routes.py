from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory, flash
from db import get_connection
from utils.logger import log_action
from middleware.auth import is_valid_session
import os
from utils.token_utils import generate_file_token, verify_file_token

UPLOAD_FOLDER = 'uploads'  
file_routes = Blueprint('files', __name__)

# @file_routes.route('/files', methods=['GET'])
# @is_valid_session
# def list_files():
#     if 'user_id' not in session:
#         return redirect(url_for('auth.login'))

#     user_id = session['user_id']
#     conn = get_connection(0)
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("""
#         SELECT d.DocumentID, d.FilePath, d.UploadTimestamp, a.AccessLevel
#         FROM pdfdocument d
#         JOIN accesscontrol a ON d.DocumentID = a.DocumentID
#         WHERE a.MemberID = %s
#     """, (user_id,))
#     files = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return render_template('files.html', files=files)


@file_routes.route('/files', methods=['GET'])
@is_valid_session
def list_files():
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

    return render_template('files.html', files=files, generate_file_token=generate_file_token)



# @file_routes.route('/files/<int:document_id>', methods=['GET'])
# @is_valid_session
# def view_file(document_id):
#     if 'user_id' not in session:
#         flash('You must be logged in to access files.')
#         return redirect(url_for('auth.login'))

#     user_id = session['user_id']
#     conn = get_connection(0)
#     cursor = conn.cursor(dictionary=True)

#     # Check if the user has access to the file
#     cursor.execute("""
#         SELECT d.FilePath, a.AccessLevel
#         FROM accesscontrol a
#         JOIN pdfdocument d ON a.DocumentID = d.DocumentID
#         WHERE a.MemberID = %s AND d.DocumentID = %s
#     """, (user_id, document_id))
#     access = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if not access:
#         flash('You do not have access to this document.')
#         log_action(user_id, 'Unauthorized Attempt', 'Tried to access a restricted document', document_id)
#         return redirect(url_for('files.list_files'))

#     # Log the access attempt
#     log_action(user_id, 'View', 'Viewed document', document_id)

#     # Serve the file from the uploads folder
#     file_path = access['FilePath']
#     return send_from_directory(UPLOAD_FOLDER, os.path.basename(file_path))




@file_routes.route('/files/<token>', methods=['GET'])
def view_file(token):
    # Verify the token and extract the document ID
    document_id = verify_file_token(token)
    if not document_id:
        flash('Invalid or expired link.')
        return redirect(url_for('files.list_files'))

    user_id = session['user_id']
    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)

    # Check if the user has access to the file
    cursor.execute("""
        SELECT d.FilePath, a.AccessLevel
        FROM accesscontrol a
        JOIN pdfdocument d ON a.DocumentID = d.DocumentID
        WHERE a.MemberID = %s AND d.DocumentID = %s
    """, (user_id, document_id))
    access = cursor.fetchone()
    cursor.close()
    conn.close()

    if not access:
        flash('You do not have access to this document.')
        log_action(user_id, 'Unauthorized Attempt', 'Tried to access a restricted document', document_id)
        return redirect(url_for('files.list_files'))

    # Log the access attempt
    log_action(user_id, 'View', 'Viewed document', document_id)

    # Serve the file from the uploads folder
    file_path = access['FilePath']
    return send_from_directory(UPLOAD_FOLDER, os.path.basename(file_path))