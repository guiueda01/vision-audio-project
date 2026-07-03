import os
import logging
from datetime import datetime

def setup_logger() -> logging.Logger:
    """Configura e retorna uma instância de logger estruturada."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logger = logging.getLogger("CV_App")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        
        # Handler para arquivo rotativo simplificado por data
        file_handler = logging.FileHandler(os.path.join(log_dir, f"app_{datetime.now().strftime('%Y-%m-%d')}.log"), encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()