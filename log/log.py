import logging
import logging.config
import yaml
import os

def setup_logging():
    with open("log/logging.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    for handler in config.get('handlers', {}).values():
        if 'filename' in handler:
            log_file_path = handler['filename']
            if os.path.exists(log_file_path):
                #os.remove(log_file_path)
                print(f"Deleted existing logging file: {log_file_path}")

    logging.config.dictConfig(config)