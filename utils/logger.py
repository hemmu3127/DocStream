# utils/logger.py
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logger():
    """
    Configures and returns a root logger.
    - Logs to console.
    - Log level is configurable via .env file.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Get the root logger
    logger = logging.getLogger()
    
    # Prevent duplicate handlers if this function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(log_level)

    # Create a handler to stream logs to the console
    stream_handler = logging.StreamHandler(sys.stdout)
    
    # Create a formatter for the logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    
    # Create a handler to write logs to a file
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Initialize the logger once
log = setup_logger()