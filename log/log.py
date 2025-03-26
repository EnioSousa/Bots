import logging
import logging.config
import yaml
import os
import sys

def setup_logging():
    # Determine the correct path for the logging configuration
    if getattr(sys, 'frozen', False):
        logging_yaml_path = os.path.join(sys._MEIPASS, 'log', 'logging.yaml')
    else:
        logging_yaml_path = os.path.join(os.path.dirname(__file__), 'logging.yaml')
    
    # Load the logging configuration
    with open(logging_yaml_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Remove existing log files if they exist
    for handler in config.get('handlers', {}).values():
        if 'filename' in handler:
            log_file_path = handler['filename']
            if os.path.exists(log_file_path):
                os.remove(log_file_path)
                print(f"Deleted existing logging file: {log_file_path}")

    # Apply the logging configuration
    logging.config.dictConfig(config)
