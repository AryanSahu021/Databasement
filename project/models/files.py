from db import get_connection

def upload_file(member_id, file_name, file_path, encryption_key):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO documents (filename, file_path, encryption_key, uploaded_by)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (file_name, file_path, encryption_key, member_id))
    conn.commit()
    file_id = cursor.lastrowid
    # Insert default access control record; owner gets full permissions.
    access_query = """
        INSERT INTO document_access (document_id, user_id, access_level, granted_by)
        VALUES (%s, %s, 'owner', %s)
    """
    cursor.execute(access_query, (file_id, member_id, member_id))
    conn.commit()
    cursor.close()
    conn.close()
    return file_id

def get_user_files(member_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.* FROM documents d
        JOIN document_access a ON d.id = a.document_id
        WHERE a.user_id = %s AND a.access_level IN ('owner', 'edit', 'view')
    """
    cursor.execute(query, (member_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_file_access(file_id, target_member_id, can_view, can_edit, can_share):
    conn = get_connection()
    cursor = conn.cursor()
    # Determine access level based on booleans.
    if can_share or can_edit:
        access_level = 'edit'
    elif can_view:
        access_level = 'view'
    else:
        access_level = 'view'
    query = """
        INSERT INTO document_access (document_id, user_id, access_level, granted_by)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE access_level = VALUES(access_level)
    """
    cursor.execute(query, (file_id, target_member_id, access_level, target_member_id))
    conn.commit()
    cursor.close()
    conn.close()