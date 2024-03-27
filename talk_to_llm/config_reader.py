'''
Description: 
Author: haichun feng
Date: 2024-03-26 17:49:55
LastEditor: haichun feng
LastEditTime: 2024-03-27 14:54:26
'''

import box
import yaml

class ConfigManager:
    def __init__(self):
        self.config_data = box.Box()
        self.load_config('config.yml')

    def load_config(self,config_file):
        with open(config_file, "r", encoding="utf8") as configuration:
            cfg = box.Box(yaml.safe_load(configuration))
            self.config_data = cfg

    def get_config(self, key):
        data = self.config_data
        if key in data:
            return data[key]
        else:
            raise InvalidAgeError("Config item not exists")


if __name__ == "__main__":
    config = ConfigManager()
    print(config.get_config("AUDIO_FILES_DIRECTORY"))
    # Load_config()
    # print(get_AUDIO_FILES_DIRECTORY())