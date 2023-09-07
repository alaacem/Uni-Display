
import os
import platform

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl


class FileManager:
    def __init__(self, file_path,lock):
        self.file_path = file_path
        self.lock=lock
    def lock_file(self, file):
        if platform.system() == "Windows":
            msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, os.path.getsize(self.file_path))
        else:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)

    def unlock_file(self, file):
        try:
            msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(self.file_path))
        except PermissionError:
            print("Could not unlock the file. Permission denied.")

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
        with open(self.file_path, "r+") as file:
            content = file.read()
            new_content = update_func(content)
            file.seek(0)
            file.write(new_content)
            file.truncate()
            self.unlock_file(file)
