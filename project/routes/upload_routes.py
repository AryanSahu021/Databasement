from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_connection
import os

upload_routes = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'  # Directory to store uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_routes.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        access_level = request.form['access_level']
        folder_id = request.form['folder_id']

        if file and folder_id:
            # Save the file to the uploads folder
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Normalize the file path to use forward slashes
            normalized_file_path = file_path.replace("\\", "/")

            conn = get_connection(0)
            cursor = conn.cursor()

            # Insert file metadata into pdfdocument table
            cursor.execute("""
                INSERT INTO pdfdocument (OwnerID, FilePath)
                VALUES (%s, %s)
            """, (session['user_id'], normalized_file_path))
            document_id = cursor.lastrowid

            # Add the file to the selected folder
            cursor.execute("""
                INSERT INTO folderdocuments (FolderID, DocumentID)
                VALUES (%s, %s)
            """, (folder_id, document_id))

            # Assign access to the uploader
            cursor.execute("""
                INSERT INTO accesscontrol (DocumentID, MemberID, AccessLevel)
                VALUES (%s, %s, %s)
            """, (document_id, session['user_id'], access_level))

            conn.commit()
            cursor.close()
            conn.close()

            flash('File uploaded successfully.')
            return redirect(url_for('dashboard.dashboard'))

    # Fetch folders for the dropdown
    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT FolderID, FolderName, FolderType
        FROM folder
        WHERE MemberID = %s
    """, (session['user_id'],))
    folders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('upload.html', folders=folders)