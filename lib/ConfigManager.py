import json
import logging
import os
import shutil
class ConfigManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r",encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with open(self.file_path, "w",encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def update_value(self, key, value):
        data = self.load()
        if key not in data:
            return None
        data[key] = value
        self.save(data)
    def has_changes(self, other_config):
        current_config = self.load()
        return current_config != other_config
    def save_if_changed(config_manager, new_config):
        """Save the config only if there are changes."""
        current_config = config_manager.load()
        if current_config != new_config:
            config_manager.save(new_config)

class FixedSizeRotatingFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a+', maxBytes=0, encoding=None, delay=0):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)
        self.maxBytes = maxBytes

    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:  # Are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, os.SEEK_END)  # Go to the end of the file
            if self.stream.tell() + len(msg) > self.maxBytes:
                # Figure out how much we need to trim from the start
                trim_length = len(msg)
                self.stream.seek(0)  # Go to the start
                self.stream.read(trim_length)  # "read out" the part we want to trim
                remaining_log = self.stream.read()  # save the remaining log content
                self.stream.seek(0)
                self.stream.truncate()  # empty the file
                self.stream.write(remaining_log)
            self.stream.write(msg)
            self.stream.flush()
        else:
            logging.FileHandler.emit(self, record)

