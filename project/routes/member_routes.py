from flask import Blueprint, jsonify, request
from db import get_connection

member_routes = Blueprint('members', __name__)

@member_routes.route('/members', methods=['GET'])
def get_members():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(members)

@member_routes.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Missing name or email'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Member added successfully'})