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

    def get(self, guild, data_type, key):
        user_dict = self.data.get(guild, {}).get(data_type, {})
        return user_dict.get(key, data_type, key)

    def set(self, guild, data_type, key, value):
        if guild not in self.data:
            self.data[guild] = {}
        if data_type not in self.data[guild]:
            self.data[guild][data_type] = {}
            self.data[guild][data_type] = {}
        self.data[guild][key] = value
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def get_all_keys(self, guild, data_type):
        user_dict = self.data.get(guild, {}).get(data_type, {})
        return list(user_dict.keys())

    def delete(self, guild, data_type, key):
        if guild in self.data:
            if data_type in self.data[guild]:
                user_dict = self.data[guild][data_type]
                if key in user_dict:
                    del user_dict[key]
                    with open(self.filename, 'wb') as f:
                        pickle.dump(self.data, f)
                    return True
        return False

    def delete_all(self, guild, data_type):
        if guild in self.data:
            if data_type in self.data[guild]:
                backup_dir = 'backups'
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                backup_num = len(os.listdir(backup_dir)) + 1
                backup_filename = f"{guild}_{data_type}_{self.filename}.bak.{backup_num}"
                with open(os.path.join(backup_dir, backup_filename), 'wb') as backup_file:
                    pickle.dump(self.data[guild][data_type], backup_file)
                del self.data[guild][data_type]
                with open(self.filename, 'wb') as f:
                    pickle.dump(self.data, f)

    def to_json_string(self):
        json_data = json.dumps(self.data, indent=None)
        json_lines = json_data.replace('}', '}\n')
        return json_lines
