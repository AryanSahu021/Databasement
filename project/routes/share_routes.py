from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db import get_connection
from middleware.auth import is_valid_session

share_routes = Blueprint('share', __name__)

@share_routes.route('/shared_requests/send', methods=['POST'])
@is_valid_session
def send_shared_request():
    receiver_id = request.form.get('receiver_id')
    document_id = request.form.get('document_id')

    if not receiver_id or not document_id:
        flash('Receiver ID and Document ID are required.')
        return redirect(url_for('files.list_files'))

    sender_id = session['user_id']

    conn = get_connection(0)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sharedrequests (SenderID, ReceiverID, DocumentID, Status)
        VALUES (%s, %s, %s, 'Pending')
    """, (sender_id, receiver_id, document_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Shared request sent successfully.')
    return redirect(url_for('files.list_files'))

@share_routes.route('/shared_requests', methods=['GET'])
@is_valid_session
def list_shared_requests():
    user_id = session['user_id']

    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sr.RequestID, sr.SenderID, sr.ReceiverID, sr.DocumentID, sr.Status, sr.RequestTimestamp
        FROM sharedrequests sr
        WHERE sr.ReceiverID = %s
    """, (user_id,))
    requests = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('sharerequest.html', requests=requests)

@share_routes.route('/shared_requests/<int:request_id>/update', methods=['POST'])
@is_valid_session
def update_shared_request_status(request_id):
    status = request.form.get('status')  # e.g., 'Accepted', 'Rejected'

    if not status:
        flash('Status is required.')
        return redirect(url_for('share.list_shared_requests'))

    conn = get_connection(0)
    cursor = conn.cursor(dictionary=True)

    # Fetch the shared request details
    cursor.execute("""
        SELECT ReceiverID, DocumentID
        FROM sharedrequests
        WHERE RequestID = %s
    """, (request_id,))
    shared_request = cursor.fetchone()

    if not shared_request:
        flash('Shared request not found.')
        return redirect(url_for('share.list_shared_requests'))

    receiver_id = shared_request['ReceiverID']
    document_id = shared_request['DocumentID']

    # Update the status of the shared request
    cursor.execute("""
        UPDATE sharedrequests
        SET Status = %s
        WHERE RequestID = %s
    """, (status, request_id))

    # If the request is accepted, grant or update access to the file
    if status == 'Accepted':
        # Check if the user already has access to the file
        cursor.execute("""
            SELECT AccessLevel
            FROM accesscontrol
            WHERE DocumentID = %s AND MemberID = %s
        """, (document_id, receiver_id))
        access = cursor.fetchone()

        if access:
            # Update the access level if already present
            cursor.execute("""
                UPDATE accesscontrol
                SET AccessLevel = 'read'
                WHERE DocumentID = %s AND MemberID = %s
            """, (document_id, receiver_id))
        else:
            # Grant new access to the file
            cursor.execute("""
                INSERT INTO accesscontrol (DocumentID, MemberID, AccessLevel)
                VALUES (%s, %s, 'read')
            """, (document_id, receiver_id))

        # Check if the "Shared" folder exists for the receiver
        cursor.execute("""
            SELECT FolderID
            FROM folder
            WHERE MemberID = %s AND FolderName = 'Shared'
        """, (receiver_id,))
        shared_folder = cursor.fetchone()

        if not shared_folder:
            # Create the "Shared" folder if it doesn't exist
            cursor.execute("""
                INSERT INTO folder (MemberID, FolderName, FolderType)
                VALUES (%s, 'Shared', 'Private')
            """, (receiver_id,))
            shared_folder_id = cursor.lastrowid
        else:
            shared_folder_id = shared_folder['FolderID']

        # Add the file to the "Shared" folder
        cursor.execute("""
            INSERT INTO folderdocuments (FolderID, DocumentID)
            VALUES (%s, %s)
        """, (shared_folder_id, document_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Shared request status updated successfully.')
    return redirect(url_for('share.list_shared_requests'))