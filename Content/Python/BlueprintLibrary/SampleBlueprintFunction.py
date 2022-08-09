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
        print("Start Batch file")
        unreal_editor = unreal.Paths.root_dir() + 'Engine/Binaries/Win64/UnrealEditor.exe'
        project_dir = unreal.Paths.project_dir()
        program_dir = unreal.Paths.project_plugins_dir() + 'UnrealPyClient/Content/Python/'
        print("Unreal_Editor: "+unreal_editor)
        print("Unreal_Project: " + project_dir)
        project_dir = unreal.Paths.project_dir()[:-1]
        project_file = project_dir.split("/")[-1]
        project_file_path = unreal.Paths.project_dir() + project_file + '.uproject'
        print('File project: ' + project_file_path)
        print(program_dir + "MakeShotRenderArg.bat "+sMapName+' '+sSeqName+' '+sShotName+' "'+unreal_editor+'" "'+project_file_path+'"')
        unreal.log(
            "Execute Render Shot Bluerprint Action With Inputs {} {} {} {}".format(
                bPar, sMapName, sSeqName, sShotName
            )
        )
        os.system(program_dir + "MakeShotRenderArg.bat "+sMapName+' '+sSeqName+' '+sShotName+' "'+unreal_editor+'" "'+project_file_path+'"')

    @unreal.ufunction(ret=str)
    def unreal_project_plugin_dir(self):
        prog_dir = unreal.Paths.project_plugins_dir()
        print('Plugin Python Directory: ' + prog_dir)
        return prog_dir

    @unreal.ufunction(ret=str)
    def unreal_client_startbat(self):
        clientbat = os.getcwd()+"start_client.bat"
        os.system(clientbat)
        print('Start UnrealPy_Client! : ' + clientbat)
        return 'Start UnrealPy_Client! : ' + clientbat

    @unreal.ufunction(ret=str)
    def unreal_update_perforce(self):
        prog_dir = unreal.Paths.project_plugins_dir() + 'UnrealPyClient/Content/Python/'
        perforcebat = prog_dir + "UpdatePerforce.bat"
        print('Update Perforce! : ' + perforcebat)
        os.system(perforcebat)
        return perforcebat
