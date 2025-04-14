from db import get_connection

def get_member_portfolio(member_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM portfolio WHERE member_id = %s", (member_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def update_portfolio(member_id, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE portfolio SET description = %s WHERE member_id = %s", (description, member_id))
    conn.commit()
    cursor.close()
    conn.close()
