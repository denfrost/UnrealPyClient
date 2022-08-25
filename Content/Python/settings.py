# Os operations
import os

# Simple Save Settings by Json
import json

import logging
logging.basicConfig(filename="M2remote.log",
					format='%(asctime)s %(message)s',
					filemode='w')

# User profile folder and some
USER_FOLDER = os.environ['USERPROFILE']
Json_settings = USER_FOLDER + '/M2_RemoteCfg.json'

def get_Settings_field(field):
    with open(Json_settings, 'r') as f:
        settings_file = json.load(f)
        return settings_file[field]

def check_exist_profile():
    return (get_Settings_field('Name') != '')


def open_or_create_Settings(list={}):
    settings_file_preset = {'Name': list[0], 'User': list[1], "Pwd": list[2], 'Host': list[3], 'Depot': list[4], 'Workspace': list[5]}
    if os.path.isfile(Json_settings):
        print("Settings exist "+Json_settings)
    else:
        print("Settings not exist! Create default")
        with open(Json_settings, 'w') as f:
            json.dump(settings_file_preset, f)

def get_Settings_profile():
    with open(Json_settings, 'r') as f:
        settings_file = json.load(f)
        return settings_file

def rewrite_exist_profile(list={}):
    settings_file_preset = {'Name': list[0], 'User': list[1], "Pwd": list[2], 'Host': list[3], 'Depot': list[4],
                            'Workspace': list[5]}
    with open(Json_settings, 'w') as f:
        json.dump(settings_file_preset, f)

def get_Current_project():
    # User profile folder and some
    Json_project = USER_FOLDER + '\M2_Settings.json'
    with open(Json_project, 'r') as f:
        settings_file = json.load(f)
        return settings_file['DefaultProject']

def addlog(info,num=0):
    logger = logging.getLogger()
    if num == 0:
        logger.info(info)
    if num == 1:
        logger.warning(info)
    if num == 2:
        logger.error(info)