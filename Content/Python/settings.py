# Os operations
import os

# Simple Save Settings by Json
import json

# User profile folder and some
USER_FOLDER = os.environ['USERPROFILE']
Json_settings = USER_FOLDER + '/M2_RemoteCfg.json'

def get_Settings_field(field):
    with open(Json_settings, 'r') as f:
        settings_file = json.load(f)
        return settings_file[field]

def check_exist_profile(Name, user, pwd, host, depot, workspace):
    open_or_create_Settings(Name, user, pwd, host, depot, workspace)
    print("look " + get_Settings_field())
    if get_Settings_field() != '':
        print(get_Settings_field())

def open_or_create_Settings(Name, user, pwd, host, depot, workspace):
    settings_file_preset = {'Name': Name, 'User': user, "Pwd": pwd, 'Host': host, 'Depot': depot, 'Workspace': workspace}
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
