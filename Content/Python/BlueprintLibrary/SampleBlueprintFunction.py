#import unreal
import os

from unreal_global import settings as settings
from unreal_global import *
from unreal_global import PyClientMovie as PyClientMovie

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
            count = 0
            if '_SEQ' in str(asset.package_name): #_ANIM_SEQ
                output = output + ',' +str(asset.object_path)
        print('Size output: '+str(len(output)))
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

    @unreal.ufunction(ret=str, static=True)
    def unreal_update_perforce():
        script_dir = os.path.abspath(__file__).split('BlueprintLibrary\SampleBlueprintFunction.py')[0]
        perforcebat = script_dir + "UpdatePerforce.bat"
        perforcePy = script_dir + "perforce.py"
        print('Update Perforce! : ' + perforcebat+' '+perforcePy)
        os.system(perforcebat+' '+perforcePy)
        return perforcebat

    @unreal.ufunction(
        params=[str, int, bool],
        static=True,
        meta=dict(Category="Samples Python BlueprintFunctionLibrary"),
    )
    def unreal_python_render_images(sSeqName, iQuality=3, bFtp_transfer=True):
        Presets = ['/Game/Cinematics/MoviePipeline/Presets/Render_Settings_001.Render_Settings_001',
                   '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_002_veryLow.Render_Settings_002_veryLow',
                   '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_002_Low.Render_Settings_002_Low',
                   '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_003_VeryHigh.Render_Settings_003_VeryHigh']
        unreal.log_warning("Job Render. Make Render Images Job : "+sSeqName+' Quality : '+Presets[iQuality]+' Transfer Publish : '+str(bFtp_transfer))
        global CurrentJob
        job_work_folder = '/LIVE' #'/UnrealRenderImages'
        job_sequence_path = sSeqName
        job_name = sSeqName.split('.')[-1]
        job_anim_dir = sSeqName.split('.')[0]
        job_anim_dir = job_anim_dir.split(job_name)[0]
        job_map_dir = job_anim_dir
        # ['C:\\Users\\mostafa.ari\\LIVE\\WHM\\EPWHH\\COMMON\\RENDER\\WHM_EPWHH_SH0170',
        #/Game/SHOTS/EPWHH/SH0000/

        print(f'Job AnimDir: {job_anim_dir}')

        job_map = str(job_name).split('_SEQ')[0]
        job_map_path = job_map_dir+job_map+'.'+job_map
        user_folder = os.path.expanduser('~')

        CurrentProject = settings.get_Current_project()
        Episode = job_anim_dir.split('SHOTS/')[-1].split('/')[0]
        print(f'Job server AnimDir: {CurrentProject}/{Episode}/COMMON/RENDER/{CurrentProject}_{Episode}_{job_map}')
        server_anim_dir = f'/{CurrentProject}/{Episode}/COMMON/RENDER/{CurrentProject}_{Episode}_{job_map}'

        output_folder = user_folder+job_work_folder+server_anim_dir
        print(f'Job : Name: {job_name} SeqPath: {job_sequence_path} Map: {job_anim_dir}{job_map} OutputFolder : {output_folder} Preset : {Presets[iQuality]}')
        CurrentJob = PyClientMovie.make_render_job(job_name, job_sequence_path, job_map_path, output_folder, Presets[iQuality])
        '''
        CurrentJob = PyClientMovie.make_render_job('NewMap_Anim_SEQ', '/Game/NewMap_Anim_SEQ.NewMap_Anim_SEQ',
                                                           '/Game/NewMap_Anim.NewMap_Anim',
                                                           'C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim',
                                                           '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_003_VeryHigh.Render_Settings_003_VeryHigh')
        '''
        unreal.log_warning("Job Render. Images Job ready: " + CurrentJob.job_name + ' Transfer to Shotgun :'+str(bFtp_transfer))
        PyClientMovie.render_jobs(output_folder, bFtp_transfer)