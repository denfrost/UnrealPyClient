import unreal
import unreal_uiutils
from unreal_global import *
from unreal_utils import AssetRegistryPostLoad
unreal.log("""@

####################

Init Start up Script

####################

""")

assetregistry_pretickhandle = None

def assetregistry_postload_handle(deltaTime):
    """
        Run callback method after registry run to prevent crashed when create new asset at startupS
    """
    unreal.log_warning("..Checking Asset Registry Status...")
    if AssetRegistry.is_loading_assets():
        unreal.log_warning("..Asset registry still loading...")
    else:
        unreal.log_warning("Asset registry ready!")
        unreal.unregister_slate_post_tick_callback(assetregistry_pretickhandle)
        AssetRegistryPostLoad.run_callbacks()

assetregistry_pretickhandle = unreal.register_slate_post_tick_callback(assetregistry_postload_handle)

import BlueprintLibrary
import UserInterfaces

def reload():
    import importlib
    importlib.reload(BlueprintLibrary)
    importlib.reload(UserInterfaces)

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

unreal_uiutils.refresh()
