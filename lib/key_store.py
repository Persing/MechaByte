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

    def get(self, guild, key):
        user_dict = self.data.get(guild, {})
        return user_dict.get(key)

    def set(self, guild, key, value):
        if guild not in self.data:
            self.data[guild] = {}
        self.data[guild][key] = value
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def get_all_keys(self, guild):
        user_dict = self.data.get(guild, {})
        return list(user_dict.keys())

    def delete(self, guild, key):
        if guild in self.data:
            user_dict = self.data[guild]
            if key in user_dict:
                del user_dict[key]
                with open(self.filename, 'wb') as f:
                    pickle.dump(self.data, f)
                return True
        return False

    def delete_all(self, guild):
        if guild in self.data:
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            backup_num = len(os.listdir(backup_dir)) + 1
            backup_filename = f"{guild}_{self.filename}.bak.{backup_num}"
            with open(os.path.join(backup_dir, backup_filename), 'wb') as backup_file:
                pickle.dump(self.data[guild], backup_file)
            del self.data[guild]
            with open(self.filename, 'wb') as f:
                pickle.dump(self.data, f)

    def to_json_string(self):
        json_data = json.dumps(self.data, indent=None)
        json_lines = json_data.replace('}', '}\n')
        return json_lines
