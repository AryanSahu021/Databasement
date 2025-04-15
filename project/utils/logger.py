import logging
from datetime import datetime
from db import get_connection

def setup_logger():
    log_filename = f'logs/safedocs_{datetime.now().strftime("%Y%m%d")}.log'
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('safedocs')

def log_action(member_id, action_type, action_details, document_id=None):
    """
    Logs an action performed by a member into the auditlog table.
    """
    conn = get_connection(0)
    cursor = conn.cursor()
    try:
        # Insert into auditlog table
        cursor.execute("""
            INSERT INTO auditlog (MemberID, DocumentID, ActionType)
            VALUES (%s, %s, %s)
        """, (member_id, document_id, action_type))
        conn.commit()

        # Log to file
        logger = setup_logger()
        logger.info(f"Action logged: MemberID={member_id}, ActionType={action_type}, DocumentID={document_id}, Details={action_details}")
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Failed to log action: {e}")
    finally:
        cursor.close()
        conn.close()

def log_failed_access(member_id, document_id, reason):
    """
    Logs a failed access attempt into the failedaccessattempts table.
    """
    conn = get_connection(0)
    cursor = conn.cursor()
    try:
        # Insert into failedaccessattempts table
        cursor.execute("""
            INSERT INTO failedaccessattempts (MemberID, DocumentID, Reason)
            VALUES (%s, %s, %s)
        """, (member_id, document_id, reason))
        conn.commit()

        # Log to file
        logger = setup_logger()
        logger.warning(f"Failed access attempt: MemberID={member_id}, DocumentID={document_id}, Reason={reason}")
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Failed to log failed access attempt: {e}")
    finally:
        cursor.close()
        conn.close()

def log_authentication(member_id, ip_address, status):
    """
    Logs an authentication attempt into the authenticationlog table.
    """
    conn = get_connection(0)
    cursor = conn.cursor()
    try:
        # Insert into authenticationlog table
        cursor.execute("""
            INSERT INTO authenticationlog (MemberID, IPAddress, Status)
            VALUES (%s, %s, %s)
        """, (member_id, ip_address, status))
        conn.commit()

        # Log to file
        logger = setup_logger()
        logger.info(f"Authentication attempt: MemberID={member_id}, IPAddress={ip_address}, Status={status}")
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Failed to log authentication attempt: {e}")
    finally:
        cursor.close()
        conn.close()