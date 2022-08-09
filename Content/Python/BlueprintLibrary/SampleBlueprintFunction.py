import unreal
import os

from unreal_global import *


@unreal.uclass()
class SamplePythonBlueprintLibrary(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(
        static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def python_test_bp_action_noinput():
        unreal.log("Executed from Python!")

    @unreal.ufunction(
        params=[int, str],
        static=True,
        meta=dict(Category="Samples Python BlueprintFunctionLibrary"),
    )
    def python_test_bp_action_input(input_num, input_string):
        unreal.log(
            "Execute Bluerprint Action With Inputs {} {}".format(
                input_num, input_string
            )
        )

    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def python_test_bp_action_return():
        result = "Success !!!"
        #unreal.log("Execute Bluerprint Action Return")
        return result


    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def unreal_python_get_all_shots():
        output = ''
        asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
        assets = asset_reg.get_assets_by_class('LevelSequence', search_sub_classes=False)
        for asset in assets:
            print(asset)
            if '_Anim_SEQ' in str(asset.object_path):
                output = output + ',' +str(asset.object_path)
        return output

    @unreal.ufunction(
        params=[bool, str, str, str],
        static=True,
        meta=dict(Category="Samples Python BlueprintFunctionLibrary"),
    )
    def unreal_python_set_shot(bPar, sMapName, sSeqName, sShotName):
        unreal.log(
            "Execute Render Shot Bluerprint Action With Inputs {} {} {} {}".format(
                bPar, sMapName, sSeqName, sShotName
            )
        )
        print("Start Batch file")
        print(unreal.Paths.engine_user_dir() + "MakeShotRenderArg.bat "+sMapName+' '+sSeqName+' '+sShotName)
        os.system(unreal.Paths.convert_relative_path_to_full(
            unreal.Paths.engine_user_dir()) + "MakeShotRenderArg.bat "+sMapName+' '+sSeqName+' '+sShotName)

    @unreal.ufunction(ret=str)
    def unreal_project_plugin_dir(self):
        prog_dir = unreal.Paths.project_plugins_dir()
        print('Plugin Python Directory: ' + prog_dir)
        return prog_dir

    @unreal.ufunction(ret=str)
    def unreal_client_startbat(self):
        clientbat = os.getcwd()+"start_client.bat"
        os.system(unreal.Paths.convert_relative_path_to_full(clientbat))
        print('Start UnrealPy_Client! : ' + clientbat)
        return 'Start UnrealPy_Client! : ' + clientbat
