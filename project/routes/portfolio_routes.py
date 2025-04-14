from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db import get_connection
from middleware.auth import is_valid_session

portfolio_routes = Blueprint('portfolio', __name__)

@portfolio_routes.route('/portfolio', methods=['GET'])
@is_valid_session
def get_portfolio():
    user_id = session['user_id']
    user_role = session['role']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the GroupID (ProjectID) for the logged-in user
    cursor.execute("""
        SELECT GroupID
        FROM MemberGroupMapping
        WHERE MemberID = %s
    """, (user_id,))
    group_mapping = cursor.fetchone()

    if not group_mapping:
        flash('You are not assigned to any project.')
        return redirect(url_for('auth.logout'))

    project_id = group_mapping['GroupID']

    # Restrict access to members of the same project
    if user_role == 'admin':
        # Admins can view all members in the project
        cursor.execute("""
            SELECT m.ID AS MemberID, m.UserName, m.emailID AS Email
            FROM members m
            JOIN MemberGroupMapping mgm ON m.ID = mgm.MemberID
            WHERE mgm.GroupID = %s
        """, (project_id,))
    else:
        # Regular members can only view their own profile
        cursor.execute("""
            SELECT m.ID AS MemberID, m.UserName, m.emailID AS Email
            FROM members m
            JOIN MemberGroupMapping mgm ON m.ID = mgm.MemberID
            WHERE m.ID = %s AND mgm.GroupID = %s
        """, (user_id, project_id))

    members = cursor.fetchall()
    cursor.close()
    conn.close()

    # Render the portfolio.html template with the filtered members
    return render_template('portfolio.html', members=members, user_role=user_role)

@portfolio_routes.route('/portfolio/edit', methods=['POST'])
@is_valid_session
def edit_portfolio():
    if session['role'] != 'admin':
        flash('Access denied. Only admins can edit portfolio details.')
        return redirect(url_for('portfolio.get_portfolio'))

    data = request.get_json()
    member_id = data.get('member_id')
    name = data.get('name')
    email = data.get('email')

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch the GroupID (ProjectID) for the logged-in user
    cursor.execute("""
        SELECT GroupID
        FROM MemberGroupMapping
        WHERE MemberID = %s
    """, (session['user_id'],))
    group_mapping = cursor.fetchone()

    if not group_mapping:
        flash('You are not assigned to any project.')
        return redirect(url_for('auth.logout'))

    project_id = group_mapping['GroupID']

    # Update the member details only if they belong to the same project
    cursor.execute("""
        UPDATE members
        SET Name = %s, Email = %s
        WHERE MemberID = %s AND EXISTS (
            SELECT 1 FROM MemberGroupMapping
            WHERE MemberID = %s AND GroupID = %s
        )
    """, (name, email, member_id, member_id, project_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Portfolio updated successfully'})