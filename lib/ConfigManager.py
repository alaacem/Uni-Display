import json
import fasteners

class ConfigManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock = fasteners.InterProcessLock(self.file_path + ".lock")

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with self.lock:
            with open(self.file_path, "w", encoding="utf-8") as file:
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

    def save_if_changed(self, new_config):
        current_config = self.load()
        if current_config != new_config:
            self.save(new_config)
