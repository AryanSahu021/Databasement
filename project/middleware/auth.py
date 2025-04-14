from functools import wraps
from flask import request, jsonify
import requests

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401

        # Validate token with the central authentication API
        auth_response = requests.get(
            'http://10.0.116.125:5000/isAuth',
            headers={'Authorization': token}
        )
        if auth_response.status_code != 200:
            return jsonify({'error': 'Invalid or expired token'}), 401

        return f(*args, **kwargs)
    return decorated