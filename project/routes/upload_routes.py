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
        email_ids = request.form['email_ids'].split(',')
        access_level = request.form['access_level']

        if file:
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

            # Assign access to specified email IDs
            for email in email_ids:
                cursor.execute("SELECT MemberID FROM member WHERE Email = %s", (email.strip(),))
                user = cursor.fetchone()
                if user:
                    cursor.execute("""
                        INSERT INTO accesscontrol (DocumentID, MemberID, AccessLevel)
                        VALUES (%s, %s, %s)
                    """, (document_id, user[0], access_level))

            conn.commit()
            cursor.fetchall()
            cursor.close()
            conn.close()

            flash('File uploaded and access assigned successfully.')
            return redirect(url_for('files.list_files'))

    return render_template('upload.html')