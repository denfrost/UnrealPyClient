import os
import settings
print("""@

####################

Reload Unreal Worker Script

####################

""")

def techtests():
    print('techtests')

def forselectedassets():
    dir = 'C:/Users/denis.balikhin/LIVE/WHM/WHPTEST/COMMON/RENDER/WHM_WHPTEST_SH0070/V001'
    dir = dir.replace('/','\\')
    print('Check ['+dir+'] : '+str(os.path.exists(dir)))
    print('Check [' + dir + '] : ' + str(os.path.isdir(dir)))
    import unreal
    #selected_assets_objects = unreal.EditorUtilityLibrary.get_selected_assets()
    selected_assets = unreal.EditorUtilityLibrary.get_selected_asset_data()
    for ass in selected_assets:
        new_asset = ass.object_path
        print(new_asset)
        new_asset1 = str(new_asset).split('.')[0] +'_COPY'
        new_asset2 = str(new_asset).split('.')[1] + '_COPY'
        new_asset_path = new_asset1+'.'+new_asset2
        print(new_asset_path)
        #newass = unreal.EditorAssetLibrary.duplicate_asset(ass.object_path, new_asset_path)
        #unreal.EditorAssetLibrary.save_loaded_asset(newass, only_if_is_dirty=True)
        #unreal.EditorAssetLibrary.checkout_loaded_asset(newass)
        #unreal.EditorAssetLibrary.delete_loaded_asset(ass.get_asset())
        #unreal.EditorAssetLibrary.rename_asset(new_asset_path, ass.object_path)

def Unreal_CleanAllMemory(bPrint=False):
    import unreal
    unreal.log_warning("Start Unreal_CleanAllMemory")
    unreal.EditorLoadingAndSavingUtils().new_blank_map(save_existing_map=False)
    GameLoadedAssets = checkAllmemory(False)
    for Ga in GameLoadedAssets:
        unreal.log_warning(f'Try Unloaded from memory : [{Ga.asset_name}] Class [{Ga.asset_class}] in Path: [{Ga.object_path}] Package [{Ga.package_name}]')
        #unreal.EditorAssetLibrary.delete_loaded_asset(Ga.get_asset())


def checkAllmemory(bPrint=True):
    import unreal
    asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_all_assets()
    GameLoadedAssets = []
    for As in asset_list:
        if As.is_asset_loaded():
            if '/Game' in str(As.object_path):
                if bPrint:
                    print(f'Loaded in memory : [{As.asset_name}] Class [{As.asset_class}] in Path: [{As.object_path}]')
                GameLoadedAssets.append(As)
    unreal.log_warning(f'Detected assets [{str(len(asset_list))}] count [{str(len(GameLoadedAssets))}] in memory.')
    for GA in GameLoadedAssets:
        unreal.log_warning(f'Loaded in memory : [{GA.asset_name}] Class [{GA.asset_class}] in Path: [{GA.object_path}]')
    return GameLoadedAssets

def spawn_actor(assetpath):
    import unreal
    if unreal.EditorAssetLibrary.does_asset_exist(assetpath):
        assetobject = unreal.EditorAssetLibrary.load_asset(assetpath)
        spawn_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(assetobject, unreal.Vector(0, 0, 0))
        print('Loaded and spawned asset: %s' % spawn_actor)
        return spawn_actor

def show_funcs_unreal():
    import unreal
    for x in sorted(dir(unreal)):
        print(x)

def start():
    import unreal
    print('Start Test')
    unreal.log_warning("Start Actor")
    #Actor = spawn_actor('/Game/Test/Denis/Blueprints/BP_Actor.BP_Actor')
    #unreal.log_warning("Actor: %s" % Actor)

    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = unreal.EditorActorSubsystem.get_all_level_actors(eas)

    so_subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    for actor in actors:
        print(str(actor))
        print(str(actor.get_name()))
        if str(actor.get_class().get_name()) == 'SkeletalMeshActor':  # SkeletalMeshActor
            roots_sub_object = so_subsystem.k2_gather_subobject_data_for_instance(actor)
            count = 0
            for root in roots_sub_object:
                print('Roots #%s - %s' % (count, root))
                params_parent_handle = so_subsystem.find_handle_for_object(root, actor)
                print('Roots #%s params_parent_handle  %s' % (count, params_parent_handle))
                print('Roots #%s subobject_data  %s' % (count, so_subsystem.k2_find_subobject_data_from_handle(params_parent_handle)))
                new_subobject_params = unreal.AddNewSubobjectParams\
                (parent_handle=params_parent_handle, new_class=unreal.StaticMeshComponent)
                print('Roots #%s params  %s' % (count, new_subobject_params))
                print('Roots #%s class %s' % (count, new_subobject_params.new_class))
                print('Roots #%s handle %s' % (count, new_subobject_params.parent_handle))
                new_sub_object = so_subsystem.add_new_subobject(new_subobject_params)
                print(f"created {new_sub_object}")
                res = so_subsystem.is_valid_rename(new_sub_object[0], 'New')
                print('Roots #%s res = %s' % (count, res))
                count = count+1

    unreal.log_warning("Finished")
    return

def Start_UnrealPy_Client():
    script_dir = os.path.abspath(__file__).split('unreal_worker.py')[0]
    print('Plugin UnrealPyClient Directory: ' + script_dir)
    if os.path.exists('M:\SCRIPTS\PACKAGES\Python39\python.exe'):
        clientbat = script_dir + "start_m2client.bat"
        unreal_client_path = script_dir + 'UnrealPy_Client.py'
        os.system(clientbat+' '+unreal_client_path)
        print('Start M2 UnrealPy_Client! : ' + script_dir + "start_UnrealPy_Client.bat")
    else:
        clientbat = script_dir + "start_client.bat"
        unreal_client_path = script_dir + 'UnrealPy_Client.py'
        os.system(clientbat+' '+unreal_client_path)
        print('Start Standard UnrealPy_Client! : '+clientbat+' '+unreal_client_path)

def ShowWorkingDirs():
    import unreal
    script_dir = os.path.abspath(__file__).split('unreal_worker.py')[0]
    print('main dir program : '+script_dir)
    prog_dir = unreal.Paths.project_plugins_dir() + 'UnrealPyClient'
    print('Plugin UnrealPyClient Directory: ' + prog_dir)
    engine_dir = unreal.Paths.engine_dir()
    root_dir = unreal.Paths.root_dir()
    unreal_dir = unreal.Paths.root_dir() + 'Engine/Binaries/Win64'
    project_dir = unreal.Paths.project_dir()[:-1]
    project_file = project_dir.split("/")[-1]
    project_file_path = unreal.Paths.project_dir() + project_file+'.uproject'
    print('File project: '+project_file_path)
    video_capture_dir = unreal.Paths.video_capture_dir()
    project_persistent_download_dir = unreal.Paths.project_persistent_download_dir()
    print('extend dirs...')
    print('Unreal Directory: ' + unreal_dir)
    print('Root Directory: ' + root_dir)
    print('Binaries Directory: ' + engine_dir)
    print('Project Directory: ' + project_dir)
    print('Video Capture Directory: ' + video_capture_dir)
    print('Project Download Directory: ' + project_persistent_download_dir)

def UpdatePerforce():
    import unreal
    import BlueprintLibrary.SampleBlueprintFunction as bp_lib
    Unreal_CleanAllMemory() #becarefull sure run with perforce Update only
    bp_lib.SamplePythonBlueprintLibrary.unreal_update_perforce()

def Render_Images_Sequence():
    print('Start Images Rendering')
    #PyClient.movie_render.cleanup_queue() #Cleanup queue
    """
        SH1870
        /Game/SHOTS/WHP01/SH1870/SH1870_SEQ.SH1870_SEQ
        /Game/SHOTS/WHP01/SH1870/SH1870.SH1870
        C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim
        C:/Users/denis.balikhin/LIVE/WHM/WHP01/COMMON/RENDER/WHM_WHP01_SH1870
        /Game/Cinematics/MoviePipeline/Presets/Render_Settings_003_VeryHigh.Render_Settings_003_VeryHigh
    """
    global CurrentJob
    #CurrentJob = PyClient.movie_render.make_render_job('NewMap_Anim_SEQ', '/Game/NewMap_Anim_SEQ.NewMap_Anim_SEQ', '/Game/NewMap_Anim.NewMap_Anim', 'C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim',
    #                                     '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_003_VeryHigh.Render_Settings_003_VeryHigh')
    print_MoviePipelineQueue()
    #PyClient.movie_render.render_jobs('C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim', False)
    #delete_MoviePipelineJob('NewMap_Anim_SEQ')
    #PyClient.movie_render.make_render_job('Test', sequencer, world, output_folder, preset_addr)
    #PyClient.movie_render.render_jobs(image_dirs, transfer=False):


def print_MoviePipelineQueue():
    import unreal
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = subsystem.get_queue()

    existed_jobs = pipelineQueue.get_jobs()
    print('Current JOB name : ' + str(CurrentJob.job_name))

    print('Queue jobs count= ' + str(len(existed_jobs)))

    for job in existed_jobs:
        print('Job Seq = '+str(job.sequence))
        print('Job Map = '+str(job.map))
        print('Job Name = '+str(job.job_name))

def My_Render_Images(sequence=''):
    import unreal
    import PyClient.movie_render
    if sequence == '':
        print('Sequence null')
        return
    unreal.log_warning("Job Render. Make Render Images Job")
    global CurrentJob
    CurrentJob = PyClient.movie_render.make_render_job('NewMap_Anim_SEQ', '/Game/NewMap_Anim_SEQ.NewMap_Anim_SEQ',
                                                       '/Game/NewMap_Anim.NewMap_Anim',
                                                       'C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim',
                                                       '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_003_VeryHigh.Render_Settings_003_VeryHigh')
    unreal.log_warning("Job Render. Images Job ready: "+CurrentJob.job_name)
    PyClient.movie_render.render_jobs('C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim', False)

def openFolderImages():
    import PyClient.movie_render
    print(PyClient.movie_render.image_directories)

def getrenderingjobs():
    import PyClient.movie_render
    CurrentJobs = PyClient.movie_render.get_render_queue_jobs()
    PyClient.movie_render.is_rendering_queue()
    for job in CurrentJobs:
        print(job.job_name)
    return CurrentJobs

def M2_get_projects_dict():
    import glob
    # Projects MEME json directory
    meme_shows_path = 'M:/SHOWS'
    all_proj = glob.glob(meme_shows_path + '/*.json')
    print(meme_shows_path + '/*.json')
    for id, elem in enumerate(all_proj):
        elem = elem.replace('\\', '/')
        elem = elem.split('/')[-1].split('.')[0]
        all_proj[id] = elem
    return all_proj

def set_PluginVersion():
    version_date = settings.get_ClientSettingsByName('ClientRevisionDate')
    if len(version_date) == 0:
        return
    import unreal
    import json
    python_Uplugin_file = unreal.Paths.project_plugins_dir() +'UnrealPyClient/M2UnrealEngineRemote.uplugin'
    if os.path.isfile(python_Uplugin_file):
        with open(python_Uplugin_file, 'r') as f:
            json_Uplugin_file = json.load(f)
            unreal.log_warning('Json '+str(json_Uplugin_file))
            json_Uplugin_file["VersionName"] = version_date
            if len(json_Uplugin_file)>0:
                with open(python_Uplugin_file, 'w') as f:
                    #json_Uplugin_file = json.dump(python_Uplugin_file, f)
                    json.dump(json_Uplugin_file, f)
                    unreal.log_warning('Json ' + str(json_Uplugin_file))
    else:    unreal.log_warning('Json file Plugin not found')