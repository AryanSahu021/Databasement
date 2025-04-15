from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db import get_connection
from middleware.auth import is_valid_session
from utils.logger import log_action
from utils.token_utils import generate_file_token, verify_file_token

folder_routes = Blueprint('folder', __name__)


@folder_routes.route('/folders/add', methods=['POST'])
@is_valid_session
def add_folder():
    folder_name = request.form.get('folder_name')
    folder_type = request.form.get('folder_type')
    member_id = session['user_id']

    if not folder_name or not folder_type:
        flash('Folder name and type are required.')
        return redirect(url_for('folder.list_folders'))

    conn = get_connection(0)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO folder (MemberID, FolderName, FolderType)
        VALUES (%s, %s, %s)
    """, (member_id, folder_name, folder_type))
    conn.commit()
    cursor.close()
    conn.close()

    # Log the action
    log_action(
        member_id=member_id,
        action_type='Create Folder',
        action_details=f'Created folder "{folder_name}" of type "{folder_type}"'
    )
    flash('Folder created successfully.')
    return redirect(url_for('folder.list_folders'))


@folder_routes.route('/folders/<int:folder_id>/delete', methods=['POST'])
@is_valid_session
def delete_folder(folder_id):
    member_id = session['user_id']

    conn = get_connection(0)
    cursor = conn.cursor()

    # Check if the folder belongs to the user
    cursor.execute("""
        SELECT FolderID
        FROM folder
        WHERE FolderID = %s AND MemberID = %s
    """, (folder_id, member_id))
    folder = cursor.fetchone()

    if not folder:
        flash('Folder not found or access denied.')
        return redirect(url_for('folder.list_folders'))

    # Delete all files in the folder
    cursor.execute("""
        DELETE FROM folderdocuments
        WHERE FolderID = %s
    """, (folder_id,))

    # Delete the folder itself
    cursor.execute("""
        DELETE FROM folder
        WHERE FolderID = %s
    """, (folder_id,))
    conn.commit()
    cursor.close()
    conn.close()

    # Log the action
    log_action(
        member_id=member_id,
        action_type='Delete Folder',
        action_details=f'Deleted folder with ID {folder_id}'
    )
    flash('Folder deleted successfully.')
    return redirect(url_for('folder.list_folders'))

@folder_routes.route('/folders', methods=['GET'])
@is_valid_session
def list_folders():
    member_id = session['user_id']

    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT FolderID, FolderName, FolderType
        FROM folder
        WHERE MemberID = %s
    """, (member_id,))
    folders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('folders.html', folders=folders)

@folder_routes.route('/folders/<int:folder_id>/files', methods=['GET'])
@is_valid_session
def list_files_in_folder(folder_id):
    member_id = session['user_id']

    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.DocumentID, d.FilePath, a.AccessLevel
        FROM folderdocuments fd
        JOIN pdfdocument d ON fd.DocumentID = d.DocumentID
        LEFT JOIN accesscontrol a ON d.DocumentID = a.DocumentID AND a.MemberID = %s
        WHERE fd.FolderID = %s
    """, (member_id, folder_id))
    files = cursor.fetchall()

    # Fetch folder name for display
    cursor.execute("""
        SELECT FolderName
        FROM folder
        WHERE FolderID = %s AND MemberID = %s
    """, (folder_id, member_id))
    folder = cursor.fetchone()

    cursor.close()
    conn.close()

    if not folder:
        flash('Folder not found or access denied.')
        return redirect(url_for('folder.list_folders'))

    return render_template('files.html', files=files, folder_name=folder['FolderName'], generate_file_token=generate_file_token)