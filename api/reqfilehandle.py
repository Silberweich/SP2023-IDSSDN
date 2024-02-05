from pathlib import Path

class FileHandler():
    def __init__(self, storage_path: Path, temp_storage_path: Path):
        self.storage_path = storage_path
        self.temp_storage_path = temp_storage_path

    def getExistingPath(self):
        return [self.storage_path, self.temp_storage_path]

    def read(self):
        with open(self.file, 'r') as f:
            return f.read()

    def write(self, data):
        with open(self.file, 'w') as f:
            f.write(data)