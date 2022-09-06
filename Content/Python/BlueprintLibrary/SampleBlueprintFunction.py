import unreal
import os

from unreal_global import settings as settings
from unreal_global import *
from unreal_global import PyClientMovie as PyClientMovie

from datetime import datetime as dt

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
        unreal.log("Execute Bluerprint Action Return")
        return result


    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def unreal_python_get_all_shots():
        PyClientMovie.get_preload_assets()
        output = ''
        asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
        assets = asset_reg.get_assets_by_class('LevelSequence', search_sub_classes=False)
        for asset in assets:
            print(asset)
            count = 0
            if '_SEQ' in str(asset.package_name): #_ANIM_SEQ
                output = output + ',' +str(asset.object_path)
        output = output + ',' #delimiter data
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
        unreal.EditorLoadingAndSavingUtils().new_blank_map(save_existing_map=False)
        script_dir = os.path.abspath(__file__).split('BlueprintLibrary\SampleBlueprintFunction.py')[0]
        perforcebat = script_dir + "UpdatePerforce.bat"
        perforcePy = script_dir + "perforce.py"
        print('Update Perforce! : ' + perforcebat+' '+perforcePy)
        os.system(perforcebat+' '+perforcePy)
        return perforcebat

    @unreal.ufunction(
        ret=str,
        params=[str, str, bool],
        static=True,
        meta=dict(Category="Samples Python BlueprintFunctionLibrary"),
    )
    def unreal_python_make_render_job(sSeqName, sQuality = '', bFtp_transfer=True):
        Loaded_Presets_Dict = PyClientMovie.get_preload_assets()
        choosen_loaded_preset = None
        setname = ''
        for p in Loaded_Presets_Dict:
            if str(p) == sQuality:
                unreal.log_warning(f'Found "{str(p)}" == "{sQuality}')
                choosen_loaded_preset = Loaded_Presets_Dict[p][1]
                setname = Loaded_Presets_Dict[p][0]

        unreal.log_warning("Job Render. Make Render Images Job : "+sSeqName+' Quality : '+sQuality+' Transfer Publish : '+str(bFtp_transfer))

        job_work_folder = '/LIVE' #'/UnrealRenderImages'
        job_sequence_path = sSeqName
        # check sequencer
        job_shot_name = sSeqName.split('.')[-1]
        job_anim_dir = sSeqName.split('.')[0]
        job_anim_dir = job_anim_dir.split(job_shot_name)[0]
        job_map_dir = job_anim_dir
        # ['C:\\Users\\mostafa.ari\\LIVE\\WHM\\EPWHH\\COMMON\\RENDER\\WHM_EPWHH_SH0170',
        #/Game/SHOTS/EPWHH/SH0000/

        print(f'Job AnimDir: {job_anim_dir}')

        job_map = str(job_shot_name).split('_SEQ')[0]
        job_map_path = job_map_dir+job_map+'.'+job_map
        user_folder = os.path.expanduser('~')

        CurrentProject = settings.get_Current_project()
        Episode = job_anim_dir.split('SHOTS/')[-1].split('/')[0]
        print(f'Job server AnimDir: {CurrentProject}/{Episode}/COMMON/RENDER/{CurrentProject}_{Episode}_{job_map}')
        server_anim_dir = f'/{CurrentProject}/{Episode}/COMMON/RENDER/{CurrentProject}_{Episode}_{job_map}'

        output_folder = user_folder+job_work_folder+server_anim_dir
        print(f'Job : Name: {job_shot_name} SeqPath: {job_sequence_path} Map: {job_anim_dir}{job_map} OutputFolder : {output_folder} Preset : {sQuality}')
        job_name = f'{CurrentProject}_{Episode}_{job_map}'+'['+dt.now().strftime("%H:%M:%S")+']'

        subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        pipelineQueue = subsystem.get_queue()

        job = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        unreal.log_warning('try set_configuration done : preset ' + str(choosen_loaded_preset))
        job.set_configuration(choosen_loaded_preset)

        job.sequence = unreal.SoftObjectPath(sSeqName)  # unreal.SoftObjectPath(sequencer)
        unreal.log_warning('try set_configuration : preset ' + str(choosen_loaded_preset))
        job.map = unreal.SoftObjectPath(job_map_path)
        job.job_name = job_name
        job.author = str(setname) + ' Transfer [' + str(bFtp_transfer) + '] '
        unreal.log_warning('name : ' + job_name)
        unreal.log_warning('job name : ' + job.job_name)

        outputSetting = job.get_configuration().find_setting_by_class(unreal.MoviePipelineOutputSetting)
        # outputSetting.output_resolution = unreal.IntPoint(1920,1080)
        outputSetting.output_directory = unreal.DirectoryPath(output_folder)

        '''
        CurrentJob = PyClientMovie.make_render_job('NewMap_Anim_SEQ', '/Game/NewMap_Anim_SEQ.NewMap_Anim_SEQ',
                                                           '/Game/NewMap_Anim.NewMap_Anim',
                                                           'C:/Users/UnrealWorkstation/LIVE/NewMap_Anim/COMMON/RENDER/NewMap_Anim',
                                                           '/Game/Cinematics/MoviePipeline/Presets/Render_Settings_003_VeryHigh.Render_Settings_003_VeryHigh')
        '''
        unreal.log_warning("Job Render. Images Job ready: " + job.job_name + ' Transfer to Shotgun :'+str(bFtp_transfer))
        output = ''
        output = output + ',' + job.job_name + '-' + str(job.get_status_progress()) + '-' + job.author + ','
        return output

    @unreal.ufunction(
        params=[str], ret=str, static=True)
    def unreal_python_delete_render_job(sJobName):
        render_queue_system = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        if render_queue_system.is_rendering():
            if PyClientMovie.Current_Render_Job.job_name == sJobName:
                output = 'Failed delete : Rendering executed render with Job what you try delete : ' + sJobName
            return output
        render_queue = render_queue_system.get_queue()
        existed_jobs = render_queue.get_jobs()
        print('Try Delete Render Job: '+sJobName)
        for job in existed_jobs:
            unreal.log_warning(f'All Render Jobs: {job.job_name}')
            if sJobName == job.job_name:
                render_queue.delete_job(job)
                print('Render Job deleted : ' + str(job.job_name))
                unreal.log_warning(f'Render Job deleted : {str(job)}')
        output = 'Deleted Render Job: '+sJobName
        return output

    @unreal.ufunction(
        ret=str, static=True)
    def unreal_python_delete_all_render_jobs():
        render_queue_system = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        if render_queue_system.is_rendering():
            output = 'Failed delete all jobs: Rendering working'
            return output
        render_queue = render_queue_system.get_queue()
        existed_jobs = render_queue.get_jobs()
        if len(existed_jobs) > 0:
            render_queue.delete_all_jobs()
            return 'All render jobs deleted'
        else:
            return 'Render queue dont have any jobs'

    @unreal.ufunction(
        params=[str], ret=str, static=True)
    def unreal_python_start_render_job(sJobName):
        render_queue_system = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        if render_queue_system.is_rendering():
            output = 'Rendering executed before and also will render your Job: ' + sJobName
            return output
        print('Start Render Job: '+sJobName)
        PyClientMovie.render_selected_job(sJobName)
        output = 'Start Render Job: '+sJobName
        return output

    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def unreal_python_get_queue_jobs():
        output = ''
        CurrentJobs = PyClientMovie.get_render_queue_jobs()
        for job in CurrentJobs:
            job_outputSetting = job.get_configuration().find_setting_by_class(unreal.MoviePipelineOutputSetting)
            # outputSetting.output_resolution = unreal.IntPoint(1920,1080
            print('Setting config: ' + str(job.get_configuration()))
            print('SettingObj setting: ' + str(job_outputSetting))
            #print('Setting name : ' + str(job_outputSetting.file_name_format))
            print('JobName: '+job.job_name)
            print('JobProgress: '+str(job.get_status_progress()))
            print('JobStatus: ' + str(job.get_status_message()))
            output = output +',' + job.job_name + '-' + str(job.get_status_progress())+'-'+job.author+','
        return output

    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def unreal_python_get_info_remote():
        output_json_str = '{' \
                          '"MoviePipelineRendering":"' + str(PyClientMovie.is_rendering_queue()) + '",' \
                          '"MoviePipelineRendering2":"' + str(PyClientMovie.is_rendering_queue()) + '"' \
                                                  '}'
        return output_json_str

    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def unreal_python_get_render_presets():
        output = ''
        presets_rendering_dict = PyClientMovie.get_preload_assets()
        for pr in presets_rendering_dict:
            output = output + ',' + str(pr)
        return output

