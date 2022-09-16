# Os operations
import os

# Simple Save Settings by Json
import json

import logging

# User profile folder and some
USER_FOLDER = os.environ['USERPROFILE']
Json_settings_perforce = USER_FOLDER + '/M2_RemoteCfg.json'

logging.basicConfig(filename=USER_FOLDER + "/M2remote.log",
                    format='%(asctime)s %(message)s',
                    filemode='w', level=logging.INFO)

def get_PerforceSettingsByName(name):
    with open(Json_settings_perforce, 'r') as f:
        settings_file = json.load(f)
        return settings_file[name]

def check_exist_profile():
    return (get_PerforceSettingsByName('Name') != '')


def open_or_create_Settings(list={}):
    settings_file_preset = {'Name': list[0], 'User': list[1], "Pwd": list[2], 'Host': list[3], 'Depot': list[4], 'Workspace': list[5]}
    if os.path.isfile(Json_settings_perforce):
        print("Settings exist " + Json_settings_perforce)
    else:
        print("Settings not exist! Create default")
        with open(Json_settings_perforce, 'w') as f:
            json.dump(settings_file_preset, f)

def get_PerforceSettings_profile():
    with open(Json_settings_perforce, 'r') as f:
        settings_file = json.load(f)
        return settings_file

def rewrite_exist_profile(list):
    print(type(list))
    settings_file_preset = {'Name': list['Name'], 'User': list['User'], "Pwd": list["Pwd"], 'Host': list['Host'], 'Depot': list['Depot'],
                            'Workspace': list['Workspace']}
    with open(Json_settings_perforce, 'w') as f:
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

def get_HostServer():
    Json_remote = USER_FOLDER + '\M2_Remote.json'
    if os.path.isfile(Json_remote):
        with open(Json_remote, 'r') as f:
            settings_file = json.load(f)
            return settings_file['HostServer']

def get_ClientSettingsByName(name):
    Json_remote = USER_FOLDER + '\M2_Remote.json'
    if os.path.isfile(Json_remote):
        with open(Json_remote, 'r') as f:
            settings_file = json.load(f)
            return settings_file[name]


def set_ClientSettings(Host, RefreshQueueBool):
    print('Save in cfg : '+Host)
    Json_remote = USER_FOLDER + '\M2_Remote.json'
    settings_file_preset = {'HostServer': Host, 'RefreshQueueBool': RefreshQueueBool, "Test2": ''}
    with open(Json_remote, 'w') as f:
        json.dump(settings_file_preset, f)


def OpenLogPerforce():
    import subprocess
    Remote_log_file = USER_FOLDER + "/M2remote.log"
    subprocess.Popen(f'explorer "{USER_FOLDER}"')