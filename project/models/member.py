from db import get_connection

def create_member(member_id, name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (member_id, name, email) VALUES (%s, %s, %s)", (member_id, name, email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM members")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
