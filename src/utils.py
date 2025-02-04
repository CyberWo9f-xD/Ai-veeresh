import logging
import logging.config
import json
import os
from typing import Dict, Any

def setup_logging():
    """Configure logging with Unicode support"""
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
                'class': 'logging.Formatter'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '../logs/activity.log',
                'mode': 'a',
                'maxBytes': 1048576,
                'backupCount': 3,
                'formatter': 'detailed',
                'level': 'DEBUG',
                'encoding': 'utf-8'  # Add UTF-8 encoding here
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    })

def log_message(message: str, level: str = "INFO"):
    """Safe Unicode logging"""
    logger = logging.getLogger(__name__)
    try:
        # Try normal logging first
        processed_msg = message.encode('utf-8', 'replace').decode('utf-8')
    except UnicodeError:
        # Fallback for complex characters
        processed_msg = message.encode('ascii', 'replace').decode('ascii')
    
    level = level.upper()
    if level == "DEBUG":
        logger.debug(processed_msg)
    elif level == "INFO":
        logger.info(processed_msg)
    elif level == "WARNING":
        logger.warning(processed_msg)
    elif level == "ERROR":
        logger.error(processed_msg)
    elif level == "CRITICAL":
        logger.critical(processed_msg)
    else:
        logger.info(processed_msg)

def load_config(config_file: str) -> Dict[str, Any]:
    """Safe configuration loader with validation"""
    try:
        config_path = os.path.join(
            os.path.dirname(__file__), 
            f"../config/{config_file}"
        )
        with open(config_path, "r", encoding='utf-8') as f:
            return json.load(f)
            
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        log_message(f"Config error in {config_file}: {str(e)}", level="CRITICAL")
        raise