# src/utils/logger.py
import logging

def setup_logger():
    logging.basicConfig(
        filename='myshell.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('myshell')