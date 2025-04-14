from flask import Blueprint, request, jsonify
from models.files import upload_file, get_user_files, update_file_access

file_routes = Blueprint('files', __name__)

@file_routes.route('/files/upload', methods=['POST'])
def upload():
    data = request.get_json()
    file_id = upload_file(data['member_id'], data['file_name'], data['file_path'])
    return jsonify({"message": "File uploaded", "file_id": file_id})

@file_routes.route('/files/<member_id>', methods=['GET'])
def get_files(member_id):
    files = get_user_files(member_id)
    return jsonify(files)

@file_routes.route('/files/<file_id>/access', methods=['POST'])
def share_file(file_id):
    data = request.get_json()
    update_file_access(
        file_id,
        data['target_member_id'],
        data.get('can_view', False),
        data.get('can_edit', False),
        data.get('can_share', False)
    )
    return jsonify({"message": "Access updated"})
