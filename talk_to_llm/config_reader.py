'''
Description: 
Author: haichun feng
Date: 2024-03-26 17:49:55
LastEditor: haichun feng
LastEditTime: 2024-03-26 17:56:46
'''

import box
import yaml

AUDIO_FILES_DIRECTORY = ''

def Load_config():
    with open("config.yml", "r", encoding="utf8") as configuration:
        cfg = box.Box(yaml.safe_load(configuration))
        global AUDIO_FILES_DIRECTORY
        AUDIO_FILES_DIRECTORY = cfg.AUDIO_FILES_DIRECTORY

def Get_AUDIO_FILES_DIRECTORY():
    if AUDIO_FILES_DIRECTORY == '':
        Load_config()
    return AUDIO_FILES_DIRECTORY


if __name__ == "__main__":
    Load_config()
    print(Get_AUDIO_FILES_DIRECTORY())