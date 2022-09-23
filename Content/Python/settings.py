# Os operations
import os

# Simple Save Settings by Json
import json

import logging
# User profile folder and some
USER_FOLDER = os.environ['USERPROFILE']
# Client Log
Client_Log = USER_FOLDER + "/M2remote.log"
# User configs folder
Json_settings_client = USER_FOLDER + '\M2_Remote.json'
Json_m2_project = USER_FOLDER + '\M2_Settings.json'
Json_settings_perforce = USER_FOLDER + '/M2_RemoteCfg.json'

settings_client_default = {"HostServer": "ws://localhost:30020", "RefreshQueueBool": True, "AdvancedRenderBool": False}

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
        json_perforce_settings = json.load(f)
        return json_perforce_settings[name]

def check_exist_profile():
    return (get_PerforceSettingsByName('Name') != '')

def open_or_create_perforce_settings(list={}):
    settings_perforce_preset = {'Name': list[0], 'User': list[1], "Pwd": list[2], 'Host': list[3], 'Depot': list[4], 'Workspace': list[5]}
    if os.path.isfile(Json_settings_perforce):
        print("Settings exist " + Json_settings_perforce)
    else:
        print("Settings not exist! Create default")
        with open(Json_settings_perforce, 'w') as f:
            json.dump(settings_perforce_preset, f)

def get_PerforceSettings():
    with open(Json_settings_perforce, 'r') as f:
        json_perforce_settings = json.load(f)
        return json_perforce_settings

def rewrite_perforce_settings(list):
    print(type(list))
    settings_perforce_preset = {'Name': list['Name'], 'User': list['User'], "Pwd": list["Pwd"], 'Host': list['Host'], 'Depot': list['Depot'],
                            'Workspace': list['Workspace']}
    with open(Json_settings_perforce, 'w') as f:
        json.dump(settings_perforce_preset, f)

def get_Current_project():
    with open(Json_m2_project, 'r') as f:
        json_perforce_settings = json.load(f)
        return json_perforce_settings['DefaultProject']

def print_log(info, num=0):
    logger = logging.getLogger()
    if num == 0:
        logger.info(info)
    if num == 1:
        logger.warning(info)
    if num == 2:
        logger.error(info)

def get_ClientSettingsByName(name):
    if os.path.isfile(Json_settings_client):
        with open(Json_settings_client, 'r') as f:
            client_settings = json.load(f)
            return client_settings[name]

def set_ClientSettingsByName(name, value):
    data_set = settings_client_default
    data_set[name] = value
    if os.path.isfile(Json_settings_client):
        with open(Json_settings_client, 'w') as f:
            json.dump(data_set, f)

def OpenLogPerforce():
    import subprocess
    subprocess.Popen(f'explorer "{USER_FOLDER}"')