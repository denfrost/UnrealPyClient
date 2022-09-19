# Os operations
import os

# Simple Save Settings by Json
import json

import logging

# User profile folder and some
USER_FOLDER = os.environ['USERPROFILE']
# User configs folder
Json_settings_client = USER_FOLDER + '\M2_Remote.json'
Json_m2_project = USER_FOLDER + '\M2_Settings.json'
Json_settings_perforce = USER_FOLDER + '/M2_RemoteCfg.json'

settings_client_default = {"HostServer": "ws://localhost:30020", "RefreshQueueBool": True, "Test2": ""}

settings_m2_project_default = {"DefaultProject": "WHM", "AnotherNewSet": "value"}

settings_perforce_default = {'Name': 'deafault', 'User': 'User', "Pwd": "Pwd", 'Host': 'Host', 'Depot': 'Depot', 'Workspace': 'Workspace'}


logging.basicConfig(filename=USER_FOLDER + "/M2remote.log",
                    format='%(asctime)s %(message)s',
                    filemode='w', level=logging.INFO)

def setup_all_configs_if_need():
    if not os.path.isfile(Json_settings_client):
        with open(Json_settings_client, 'w') as f:
            json.dump(settings_client_default, f)
            print("Settings Client not exist! Create default")
    if not os.path.isfile(Json_m2_project):
        with open(Json_m2_project, 'w') as f:
            json.dump(settings_m2_project_default, f)
            print("Settings M2 not exist! Create default")
    if not os.path.isfile(Json_settings_perforce):
        with open(Json_settings_perforce, 'w') as f:
            json.dump(settings_perforce_default, f)
            print("Settings Perforce not exist! Create default")

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
    with open(Json_m2_project, 'r') as f:
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
    if os.path.isfile(Json_settings_client):
        with open(Json_settings_client, 'r') as f:
            settings_file = json.load(f)
            return settings_file['HostServer']

def get_ClientSettingsByName(name):
    if os.path.isfile(Json_settings_client):
        with open(Json_settings_client, 'r') as f:
            settings_file = json.load(f)
            return settings_file[name]


def set_ClientSettings(Host, RefreshQueueBool):
    print('Save in cfg : '+Host)
    settings_file_preset = {'HostServer': Host, 'RefreshQueueBool': RefreshQueueBool, "Test2": ''}
    with open(Json_settings_client, 'w') as f:
        json.dump(settings_file_preset, f)


def OpenLogPerforce():
    import subprocess
    Remote_log_file = USER_FOLDER + "/M2remote.log"
    subprocess.Popen(f'explorer "{USER_FOLDER}"')