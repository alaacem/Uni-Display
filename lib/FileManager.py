import fasteners

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock = fasteners.InterProcessLock(self.file_path + ".lock")

    def read_file(self):
        with self.lock:
            with open(self.file_path, "r") as file:
                content = file.read()
        return content

    def write_file(self, content):
        with self.lock:
            with open(self.file_path, "w") as file:
                file.write(content)

    def update_file(self, update_func):
        with self.lock:
            with open(self.file_path, "r+") as file:
                content = file.read()
                new_content = update_func(content)
                file.seek(0)
                file.write(new_content)
                file.truncate()
