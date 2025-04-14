import logging
from datetime import datetime

def setup_logger():
    log_filename = f'logs/safedocs_{datetime.now().strftime("%Y%m%d")}.log'
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('safedocs')

def log_action(member_id, action_type, action_details, document_id=None):
    conn = get_connection(0)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO auditlog (MemberID, DocumentID, ActionType)
        VALUES (%s, %s, %s)
    """, (member_id, document_id, action_type))
    conn.commit()
    cursor.close()
    conn.close()

def log_failed_access(member_id, document_id, reason):
    conn = get_connection(0)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO failedaccessattempts (MemberID, DocumentID, Reason)
        VALUES (%s, %s, %s)
    """, (member_id, document_id, reason))
    conn.commit()
    cursor.close()
    conn.close()