from pathlib import Path
import json


class JsonDBKeys:
    DIGI_PASSWORD = 'digi_password'
    DIGI_USERNAME = 'digi_username'


class JsonDB:
    keys = JsonDBKeys()

    def __init__(
            self,
            *args,
            path: str = './json_db.json',
            encoding: str = 'utf-8',
            **kwargs
    ):
        self.path = path
        self.encoding = encoding

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


jdb = JsonDB()

__all__ = [
    'jdb',
]
