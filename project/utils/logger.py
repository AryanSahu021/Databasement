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

def log_action(user_id, action_type, action_details, document_id=None):
    logger = setup_logger()
    logger.info(f"User {user_id} - {action_type} - {action_details} - Document: {document_id}")