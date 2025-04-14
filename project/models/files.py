from db import get_connection

def upload_file(member_id, file_name, file_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (member_id, file_name, file_path) VALUES (%s, %s, %s)",
                   (member_id, file_name, file_path))
    conn.commit()
    file_id = cursor.lastrowid
    cursor.execute("INSERT INTO access_control (file_id, member_id, can_view, can_edit, can_share) VALUES (%s, %s, TRUE, TRUE, TRUE)",
                   (file_id, member_id))
    conn.commit()
    cursor.close()
    conn.close()
    return file_id

def get_user_files(member_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT f.* FROM files f
        JOIN access_control a ON f.file_id = a.file_id
        WHERE a.member_id = %s AND a.can_view = TRUE
    """
    cursor.execute(query, (member_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_file_access(file_id, target_member_id, can_view, can_edit, can_share):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO access_control (file_id, member_id, can_view, can_edit, can_share)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        can_view = VALUES(can_view),
        can_edit = VALUES(can_edit),
        can_share = VALUES(can_share)
    """, (file_id, target_member_id, can_view, can_edit, can_share))
    conn.commit()
    cursor.close()
    conn.close()
