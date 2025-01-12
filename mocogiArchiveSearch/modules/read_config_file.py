import yaml
import os
import logging
from django.conf import settings


class ReadConfigFile:
    def __init__(self, file_name='config.yml', folder_name=''):
        self.file_name = file_name
        self.folder_name = folder_name

    def read_file(self, default=None):
        try:
            file_path = os.path.join(settings.BASE_DIR, self.folder_name, self.file_name)
            with open(file_path, 'r') as yaml_file:
                return yaml.safe_load(yaml_file)
        except FileNotFoundError:
            logging.error(f"File {self.file_name} not found in folder {self.folder_name}.")
            return default
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file {self.file_name}: {e}")
            return default
