from pathlib import Path
import json


class JsonDB:
    encoding = 'utf-8'
    path = './json_db.json'

    def __init__(self):
        p = Path(self.path)
        if p.is_file():
            with open(self.path, 'r', encoding=self.encoding) as file:
                self.db = json.load(file)
        else:
            self.db = {}
            self._write()

    def get(self, key):
        return self.db.get(key)

    def set(self, key, value):
        self.db[key] = value
        self._write()

    def _write(self):
        with open(self.path, 'w', encoding=self.encoding) as file:
            json.dump(self.db, file)
