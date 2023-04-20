import pickle
import os
import json


class KeyValueStore:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        try:
            with open(self.filename, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            pass

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def get_all_keys(self):
        return list(self.data.keys())

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            with open(self.filename, 'wb') as f:
                pickle.dump(self.data, f)
            return True
        else:
            return False

    def delete_all(self):
        backup_filename = self.filename + '.bak'
        os.rename(self.filename, backup_filename)
        self.data.clear()
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def to_json_string(self):
        json_data = json.dumps(self.data, indent=None)
        json_lines = json_data.replace('}', '}\n')
        return json_lines
