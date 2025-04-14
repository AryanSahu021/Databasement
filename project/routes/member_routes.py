from flask import Blueprint, request, jsonify
from models.member import create_member, delete_member, get_all_members

member_routes = Blueprint('members', __name__)

@member_routes.route('/members', methods=['GET'])
def list_members():
    members = get_all_members()
    return jsonify(members)

@member_routes.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    create_member(data['member_id'], data['name'], data['email'])
    return jsonify({"message": "Member created"})

@member_routes.route('/members/<member_id>', methods=['DELETE'])
def remove_member(member_id):
    delete_member(member_id)
    return jsonify({"message": "Member deleted"})
