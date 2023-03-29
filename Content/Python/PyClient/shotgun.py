import sys
import ssl
import getpass

import unreal

from operator import itemgetter

p = "M:/SCRIPTS"
if p not in sys.path:
    sys.path.append(p)

from MEME.api import shotgun

sg = shotgun.connect("pts_to_meme")
ssl._create_default_https_context = ssl._create_unverified_context

nameOfTask = "model_ue"
nameOfTask2 = "surface_ue"
status_UE_imported = "aprv"

def make_project_list():
    #list all active projects
    projects = sg.find('Project', filters=[['sg_status', 'is', 'Active']], fields=['code', 'name', 'id', 'sg_status'])
    unreal.log(projects)
    return projects


def make_shot_list(project, episode):
    
      
    shots = sg.find('Shot',[['project.Project.name','is',project]],['code','sg_cut_duration'])
    ret_shots = {}
    for shot in shots:
        shot_code = shot['code'].split('_')[1]
        if shot_code == episode:
            shot_name = shot['code'].split('_')[-1]
            ret_shots[shot_name] = shot['sg_cut_duration']

    return ret_shots

def get_cut_duration(shot):
    shot = 'WHK_EP2101_' + shot
    cutDuration = sg.find_one('Shot',[['project.Project.name','is','WH_40K_team'],['code','is',shot]],['sg_cut_duration'])
    return cutDuration

def find_task(asset_id, task_name):
    # Find task
    filters = [
        ['entity', 'is', {'type': 'Asset', 'id': asset_id}],
        ['content', 'is', task_name]
    ]
    task = sg.find("Task", filters, ["content", "sg_status_list"])
    return task


def change_status(task, status):
    # Change the status linked to that task
    data = {
        'sg_status_list': status
    }
    result = sg.update('Task', task, data)
    if all(elem is None for elem in result):
        return


#update Shotgun status when asset imported
def change_shotgun_status(asset):
    #List all WHK assets
    #assets = sg.find('Asset',[['project.Project.name','is','WH_40K_team']],['code'])

    #Find asset
    asset = sg.find_one("Asset", [["code", "is", asset]], ["content"])
    if all(elem is None for elem in asset):
        return

    #Find task / change task status
    task = find_task(asset['id'],'model_ue')
    if len(task)>0:
        change_status(task[0]['id'],status_UE_imported)
    task = find_task(asset['id'],'surface_ue')
    if len(task)>0:
        change_status(task[0]['id'],status_UE_imported)
    else:
        task = find_task(asset['id'],'sueface_ue')
        if len(task) > 0:
            change_status(task[0]['id'], status_UE_imported)

def publish_turntable(asset_name,movie_path):
    '''
    publish turntable movie to shotgun 
    '''
    
    project = sg.find_one('Project',[['name','is','Warhammer project']], ["content"] )
    asset = sg.find_one("Asset", [["code", "is", asset_name]], ["content"])
    task = find_task(asset['id'],'shaderUE_md')
    print(task)
    if not task:
        data = {
            'project': project,
            'content': 'ShaderUE_md',
            'entity': asset,
            'sg_status_list': 'noaprv',
            'step': {'type': 'Step', 'id': 12}
            
        }
        
        t = sg.create('Task', data)
        task = [t]
        
    
    versions = sg.find("Version", [["entity", "is", asset], ["sg_task", "is", task]], ["code"])
    
    if not versions: # the first version
        
        str_ver = '001'

    else: # find the latest version
        ver = []
        for v in  versions:
            
            str_ver = v['code']
            if '.V' in str_ver:
                str_ver = str_ver.split('.')[1]
                ver.append(int(str_ver[1:4]))
        
        if ver:
            last_ver = max(ver)
            last_ver += 1
        else:
            last_ver = 1
        
        str_ver = f'{last_ver:03d}'

    version_name = f'{asset_name}_UETURNTABLE.V{str_ver}.R001'
    
    username = getpass.getuser()
    filters = [['login', 'is', username]]
    user = sg.find_one('HumanUser', filters)
    
    data = { 'project': project,
             'code':  version_name ,
             'description': 'turntable published',
             'sg_path_to_movie': movie_path,
             'sg_status_list': 'noaprv',
             'entity': asset,
             'sg_task': {'type': 'Task', 'id' : task[0]['id']},
             'user': {'type': 'HumanUser', 'id': user['id']} 
             }
   
    version = sg.find_one("Version", [["code", "is", version_name]])
    
    
    if not version:
        result = sg.create('Version', data)
        result2 = sg.upload("Version", result['id'], movie_path, "sg_uploaded_movie") 

    # else:
                
    #     result2 = sg.upload("Version", version['id'], movie_path, "sg_uploaded_movie")
    

def publish_shot(shot_name,movie_path):
    '''
    publish shot movie to shotgun 
    '''
    unreal.log_warning('Job Render. Publish Meme. Shot_name : '+shot_name+' movie_path : '+movie_path)
    #shot_name = 'WHM_EPWHH_SH0010'

    unreal.log_warning('Job Render. Publish Meme. Finding... in sg'+str(sg))
    make_project_list()

    project = sg.find_one('Project',[['name','is','Warhammer project']], ["content"] )
    unreal.log_warning('Job Render. Publish Meme. project : '+str(project))
    shot = sg.find_one("Shot", [["code", "is", shot_name]], ["content"])
    unreal.log_warning('Job Render. Publish Meme. shot : ' + str(shot))
    task = sg.find_one("Task", [["entity", "is", shot], ["content", "is", "lighting"]])
    unreal.log_warning('Job Render. Publish Meme. project : ' + str(task))
    versions = sg.find("Version", [["entity", "is", shot], ["sg_task", "is", task]], ["code"])
    unreal.log_warning('Job Render. Publish Meme. project : ' + str(versions))

    unreal.log_warning('Job Render. Publish Meme. project : ' + str(project) + ' task : ' + str(task)+' versions : '+str(versions))

    if not versions: # the first version
        unreal.log_warning('Job Render. Publish Meme. Dont have version get  the first version')
        str_ver = '001'

    else: # find the latest version
        ver = []
        for v in  versions:
            str_ver = v['code']
            if '.V' in str_ver:
                str_ver = str_ver.split('.')[1]
                unreal.log_warning('Job Render. Publish Meme. Preparing version :'+str_ver)
                if len(str_ver):
                    ver.append(int(str_ver[1:4]))
       
        if ver:
            last_ver = max(ver)
            last_ver += 1
        else:
            last_ver = 1
        
        str_ver = f'{last_ver:03d}'

    version_name = f'LGT_{shot_name}.V{str_ver}.R001'
    
    username = getpass.getuser()
    filters = [['login', 'is', username]]
    user = sg.find_one('HumanUser', filters)
    
    data = { 'project': project,
            'code':  version_name ,
            'description': 'Unreal Render Published',
            'sg_path_to_movie': movie_path,
            'sg_status_list': 'noaprv',
            'entity': shot,
            'sg_task': {'type': 'Task', 'id' : task['id']},
            'user': {'type': 'HumanUser', 'id': user['id']} 
            }

    unreal.log_warning('Job Render. Publish Meme. meme data for create in shotgun : ' + str(data))
    result = sg.create('Version', data)
    result2 = sg.upload("Version", result['id'], movie_path, "sg_uploaded_movie")

    return str_ver

if __name__ == '__main__':
    #change_shotgun_status('WHK_PROP_DEBRIS_B')
    pass



