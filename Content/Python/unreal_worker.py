from unreal_global import *
import os
import BlueprintLibrary.SampleBlueprintFunction as bp_lib
unreal.log("""@

####################

Init Worker Script

####################

""")

def spawn_actor(assetpath):
    if unreal.EditorAssetLibrary.does_asset_exist(assetpath):
        assetobject = unreal.EditorAssetLibrary.load_asset(assetpath)
        spawn_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(assetobject, unreal.Vector(0, 0, 0))
        print('Loaded and spawned asset: %s' % spawn_actor)
        return spawn_actor

def show_funcs_unreal():
    for x in sorted(dir(unreal)):
        print(x)

def start():
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
    prog_dir = unreal.Paths.project_plugins_dir() + 'UnrealPyClient/Content/Python/'
    print('Plugin UnrealPyClient Directory: ' + prog_dir)
    clientbat = prog_dir + "start_client.bat"
    unreal_client_path = prog_dir + 'UnrealPy_Client.py'
    os.system(clientbat+' '+unreal_client_path)
    print('Start UnrealPy_Client! : '+clientbat+' '+unreal_client_path)

def ShowWorkingDirs():
    print('main dir program')
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
    bp_lib.SamplePythonBlueprintLibrary.unreal_update_perforce()

def Set_Profile_Perforce():
    unreal.EditorDialog.show_message('Error loading %s' % level_anim, 'Does not exist', unreal.AppMsgType.OK)
