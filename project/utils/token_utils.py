from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_file_token(document_id):
    """Generate a secure token for accessing a file."""
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps({'document_id': document_id}, salt='file-access')

def verify_file_token(token):
    """Verify the token and extract the document ID."""
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    try:
        data = serializer.loads(token, salt='file-access', max_age=3600)  # Token valid for 1 hour
        return data['document_id']
    except Exception:
        return None