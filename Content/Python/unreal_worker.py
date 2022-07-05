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

def start():
    print('Start Test')
    unreal.log_warning("Start Actor")
    Actor = spawn_actor('/Game/Test/Denis/Blueprints/BP_Actor.BP_Actor')
    unreal.log_warning("Actor: %s" % Actor)

    unreal.log_warning("Finished")
    return