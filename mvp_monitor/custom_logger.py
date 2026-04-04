import logging
import os

def get_logger(name="MVP_MONITOR"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        
        # Stream Handler (Console)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler (Project Root)
        log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log.txt')
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger

logger = get_logger()
