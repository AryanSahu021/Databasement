from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory, flash
from db import get_connection
from utils.logger import log_action, log_failed_access
from middleware.auth import is_valid_session
import os
from utils.token_utils import generate_file_token, verify_file_token

UPLOAD_FOLDER = 'uploads'  
file_routes = Blueprint('files', __name__)


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
        log_failed_access(member_id=user_id, document_id=document_id, reason='Unauthorized access')
        flash('You do not have access to this document.')
        log_action(user_id, 'Unauthorized Attempt', 'Tried to access a restricted document', document_id)
        return redirect(url_for('files.list_files'))
    log_action(
        member_id=user_id,
        action_type='ViewFile',
        action_details=f'User viewed file with DocumentID={document_id}',
        document_id=document_id
    )

    # Serve the file from the uploads folder
    file_path = access['FilePath']
    return send_from_directory(UPLOAD_FOLDER, os.path.basename(file_path))

@file_routes.route('/files/<int:document_id>/delete', methods=['POST'])
@is_valid_session
def delete_file(document_id):
    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)

    # Check if the user has edit access to the file
    cursor.execute("""
        SELECT FilePath
        FROM pdfdocument d
        JOIN accesscontrol a ON d.DocumentID = a.DocumentID
        WHERE d.DocumentID = %s AND a.MemberID = %s AND a.AccessLevel = 'Edit'
    """, (document_id, session['user_id']))
    file = cursor.fetchone()

    if not file:
        flash('You do not have permission to delete this file.')
        return redirect(url_for('files.list_files'))

    # Delete references to the file in related tables
    cursor.execute("DELETE FROM accesscontrol WHERE DocumentID = %s", (document_id,))
    cursor.execute("DELETE FROM folderdocuments WHERE DocumentID = %s", (document_id,))

    # Delete the file from the pdfdocument table
    cursor.execute("DELETE FROM pdfdocument WHERE DocumentID = %s", (document_id,))

    # Remove the file from the filesystem
    try:
        os.remove(file['FilePath'])
    except FileNotFoundError:
        flash('File not found on the server, but database entries were removed.')

    conn.commit()
    cursor.close()
    conn.close()

    log_action(
        member_id=session['user_id'],
        action_type='DeleteFile',
        action_details=f'User deleted file with DocumentID={document_id}'
    )

    flash('File and all its references were deleted successfully.')
    return redirect(url_for('files.list_files'))