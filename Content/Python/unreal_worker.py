import unreal
import unreal_uiutils
from unreal_global import *
from unreal_utils import AssetRegistryPostLoad
unreal.log("""@

####################

Init Worker Script

####################

""")

import BlueprintLibrary
import UserInterfaces

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