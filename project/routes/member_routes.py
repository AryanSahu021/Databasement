from flask import Blueprint, jsonify, request, session, redirect, url_for, flash
from db import get_connection
import os

member_routes = Blueprint('members', __name__)

@member_routes.route('/members/<int:member_id>', methods=['POST','DELETE'])
def delete_member(member_id):
    # Connect to the `cims` database
    conn_cims = get_connection()
    cursor_cims = conn_cims.cursor(dictionary=True)

    # Check if the member is associated with any group in the `cims` database
    cursor_cims.execute("SELECT GroupID FROM MemberGroupMapping WHERE MemberID = %s", (member_id,))
    group_mapping = cursor_cims.fetchone()

    if group_mapping:
        # If the member is associated with a group, remove the mapping
        cursor_cims.execute("DELETE FROM MemberGroupMapping WHERE MemberID = %s", (member_id,))
        conn_cims.commit()
        cursor_cims.close()
        conn_cims.close()
        return jsonify({'message': 'Member removed from group mapping successfully'})
    else:
        # If the member is not associated with any group, delete the member and their files
        # Connect to the other database
        conn_other = get_connection(0)
        cursor_other = conn_other.cursor(dictionary=True)

        # Delete files owned by the member
        cursor_other.execute("SELECT FilePath FROM pdfdocument WHERE OwnerID = %s", (member_id,))
        files = cursor_other.fetchall()
        for file in files:
            file_path = file['FilePath']
            try:
                os.remove(file_path)  # Remove the file from the filesystem
            except FileNotFoundError:
                pass  # Ignore if the file does not exist

        # Delete the member's files from the `pdfdocument` table
        cursor_other.execute("DELETE FROM pdfdocument WHERE OwnerID = %s", (member_id,))

        # Delete the member's access control entries
        cursor_other.execute("DELETE FROM accesscontrol WHERE MemberID = %s", (member_id,))

        cursor_other.execute("DELETE FROM member WHERE MemberID = %s", (member_id,))

        # Delete the member from the `members` table in the `cims` database
        cursor_cims.execute("DELETE FROM members WHERE ID = %s", (member_id,))

        # Delete the member's login credentials from the `Login` table in the `cims` database
        cursor_cims.execute("DELETE FROM Login WHERE MemberID = %s", (member_id,))
        
        conn_cims.commit()
        conn_other.commit()
        # Close all connections
        cursor_other.close()
        conn_other.close()
        cursor_cims.close()
        conn_cims.close()

        return jsonify({'message': 'Member and their files deleted successfully'})

@member_routes.route('/members/delete_self', methods=['POST'])
def delete_self():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to delete your account.')
        return redirect(url_for('auth.login'))

    confirmation = request.form.get('confirmation', 'no')
    if confirmation.lower() != 'yes':
        flash('Account deletion not confirmed.')
        return redirect(url_for('dashboard.dashboard'))

    # Connect to the `cims` database
    conn_cims = get_connection()
    cursor_cims = conn_cims.cursor(dictionary=True)

    # Connect to the other database
    conn_other = get_connection(0)
    cursor_other = conn_other.cursor(dictionary=True)

    # Delete files owned by the user
    cursor_other.execute("SELECT FilePath FROM pdfdocument WHERE OwnerID = %s", (user_id,))
    files = cursor_other.fetchall()
    for file in files:
        file_path = file['FilePath']
        try:
            os.remove(file_path)  # Remove the file from the filesystem
        except FileNotFoundError:
            pass  # Ignore if the file does not exist

    # Delete the user's files from the `pdfdocument` table
    cursor_other.execute("DELETE FROM pdfdocument WHERE OwnerID = %s", (user_id,))

    # Delete the user's access control entries
    cursor_other.execute("DELETE FROM accesscontrol WHERE MemberID = %s", (user_id,))

    cursor_other.execute("DELETE FROM member WHERE MemberID = %s", (user_id,))

    # Delete the user from the `members` table in the `cims` database
    cursor_cims.execute("DELETE FROM members WHERE ID = %s", (user_id,))

    # Delete the user's login credentials from the `Login` table in the `cims` database
    cursor_cims.execute("DELETE FROM Login WHERE MemberID = %s", (user_id,))

    conn_cims.commit()
    conn_other.commit()
    # Close all connections
    cursor_other.close()
    conn_other.close()
    cursor_cims.close()
    conn_cims.close()

    # Clear the session and redirect to the login page
    session.clear()
    flash('Your account has been deleted successfully.')
    return redirect(url_for('auth.login'))