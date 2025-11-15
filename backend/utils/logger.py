"""
Structured logging utility for Fever Oracle backend
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime

def setup_logger(name='fever_oracle', level=logging.INFO):
    """Setup structured JSON logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler with JSON formatter
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Global logger instance
logger = setup_logger()

