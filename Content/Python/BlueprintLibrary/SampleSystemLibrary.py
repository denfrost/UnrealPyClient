from unreal_global import *
import unreal_utils
import unreal

@unreal.uclass()
class SampleSystemLibrary(unreal.SystemLibrary):

        @unreal.ufunction(
            static=True,
            meta=dict(CallInEditor=True, Category="Python SystemLibrary"),
        )
        def python_system_quiteditor():
            #unreal.SystemLibrary.execute_console_command()
            unreal.SystemLibrary.execute_console_command(unreal.EditorLevelLibrary.get_editor_world(), 'QUIT_EDITOR')
            unreal.log("Execute SystemLibrary Function")

        @unreal.ufunction(static=True,meta=dict(CallInEditor=True, Category="Python SystemLibrary"),)
        def python_system_Groom_Enable():
            unreal.SystemLibrary.execute_console_command(unreal.EditorLevelLibrary.get_editor_world(), 'r.HairStrands.Enable 1')
        @unreal.ufunction(static=True, meta=dict(CallInEditor=True, Category="Python SystemLibrary"), )
        def python_system_Groom_Disable():
            unreal.SystemLibrary.execute_console_command(unreal.EditorLevelLibrary.get_editor_world(), 'r.HairStrands.Enable 0')

#classmethod execute_console_command(world_context_object, command, specific_player=None) → None¶
#Executes a console command, optionally on a specific controller
#Parameters
#world_context_object (Object) –
#command (str) – Command to send to the console
#specific_player (PlayerController) – If specified, the console command will be routed through the specified player
