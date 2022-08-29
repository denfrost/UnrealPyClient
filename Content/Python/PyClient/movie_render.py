import glob
import time
import subprocess
from pathlib import Path
import os
import shutil

import unreal

from . import utils
from . import ftp_transfer

print("Try load: Meme and  handle ImportError:")
try:
    from . import shotgun
except ImportError as ie:
    print("Try load: It cannot import module and submodule", ie)



import importlib
importlib.reload(utils)
importlib.reload(ftp_transfer)


#global image_directories
image_directories = []

def file_transfer_callback(inJob, success):

    # sleep for 2 secons to all files be written to disk
    time.sleep(3)

    # image_directories
    # ['C:\\Users\\mostafa.ari\\LIVE\\WHM\\EPWHH\\COMMON\\RENDER\\WHM_EPWHH_SH0170', 
    # 'C:\\Users\\mostafa.ari\\LIVE\\WHM\\EPWHH\\COMMON\\RENDER\\WHM_EPWHH_SH0180']

    # new
    # C:\\UserFolder\\LIVE\\CurrentProject\\EPWHH\'\COMMON\\RENDER\'\ShotnameFolder  *.exr
    # C:\\UserFolder\\LIVE\\CurrentProject\\EPWHH\'\COMMON\\MEDIA\'\ShotnameFolder  *.mp4

    print('Start Transferring Files ...')

    medias = []
    shotgun_media = []

    unreal.log_warning('Job Render. image_directories : '+str(image_directories))

    #for dir in image_directories:

    #C:\Users\UnrealWorkstation / LIVE / WHM / EPWHH / COMMON / RENDER / WHM_EPWHH_SH0000
    full_name_shot = image_directories.split('/')[-1]
    name_shot = image_directories.split('_')[-1]
    unreal.log_warning('Full name shot : '+full_name_shot)
    #image_seq = dir + '\\' + dir.split('_')[-1] + '_SEQ.%04d.exr'

    image_seq = image_directories +'/'+ name_shot + '_SEQ.%04d.exr'
    unreal.log_warning('Job Render. image_seq : ' + str(image_seq))
    #tl = dir.split('\\')[:-2]
    #output_folder = '/'.join(tl) + '/MEDIA'
    movie_dir = image_directories.split('RENDER/')[0]
    output_folder = movie_dir + '/MEDIA'
    folder = Path(output_folder)
    if not folder.exists ():
        os.makedirs(folder)
        
    # make media for shotgun
    output_mov = output_folder + '/' + 'UER_' + full_name_shot + '.mp4'

    unreal.log_warning('Job Render. output_mov : '+str(output_mov))

    #conversion_cmd = f'ffmpeg -y -start_number 101 -i {image_seq} -c:v libx264 -crf 18 -vb 20M -vf fps=25 -pix_fmt yuv420p {output_mov}'
        
    conversion_cmd = f'ffmpeg -y -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -start_number 101 -i {image_seq} -c:v libx264  -vf "lutrgb=r=gammaval(0.416666667):g=gammaval(0.416666667):b=gammaval(0.416666667)" -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -crf 18 -vb 20M {output_mov}'
        
    print (conversion_cmd)
    CREATE_NO_WINDOW = 0x08000000
    subprocess.call( conversion_cmd,creationflags=CREATE_NO_WINDOW)

    unreal.log_warning('Job Render. conversion_cmd : ' + str(conversion_cmd))
    of = Path(output_mov)
    if of.exists():
        # send media file to L drive
        l_drive_media = ftp_transfer.transfer_data([output_mov])

        # publish it to shotgun
        time.sleep(3)

        unreal.log_warning('Get version shotgun before TRY..')
        try:
            unreal.log_warning('Job Render. Get version shotgun')
            version = shotgun.publish_shot(name_shot, l_drive_media[0])
            print('MSH :'+str(version))
        except:
            print('error in submit to shotgun')
            version = '001'
        else:
            unreal.log_warning('Job Render. Get version shotgun of not exist..')

    # transfer rendered frames to Render folder in L
    # duplicate for version first
        
    files_list = []
    unreal.log_warning('Frames dir : '+output_folder)
    files = glob.glob(image_directories + '/*')
        
    if len(files):
        folder = f'{image_directories}/V{version}'
        if not os.path.exists(folder):
            os.makedirs(folder)

        for f in files:
            copied_file = shutil.copy2(f, folder)
            files_list.append(copied_file)

                # add hero file
        files_list.extend(files)

        l_drive_files = ftp_transfer.transfer_data(files_list)
        

def cleanup_queue():
    '''
    Cleanup the queue by deleting existing jobs
   
    '''
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = subsystem.get_queue()
    
    existed_jobs = pipelineQueue.get_jobs()

    for job in existed_jobs:
        pipelineQueue.delete_job(job)


def make_render_job(name,sequencer, world,output_folder,preset_addr):
    '''
    Add a render job to render queue

    Parameters:
                name (str): name of the job
                sequencer (str): address of sequencer asset to be used in this job
                world (str): address of the map asset to be used in this job
                output_folder (str): address of folder the images save there
                preset_addr (str): the preset setting to be used in this job
    
    '''
    
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = subsystem.get_queue()
    
    job = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
    preset = utils.load_asset(preset_addr)
    job.set_configuration(preset)
    
    job.sequence = unreal.SoftObjectPath(sequencer)
    job.map = unreal.SoftObjectPath(world)
    job.job_name  = name
    
    outputSetting = job.get_configuration().find_setting_by_class(unreal.MoviePipelineOutputSetting)
    #outputSetting.output_resolution = unreal.IntPoint(1920,1080)
    outputSetting.output_directory = unreal.DirectoryPath(output_folder)
    return job


def render_jobs(image_dirs,transfer=False):
    '''
    Render jobs already in render queue

    Parameters:
                image_dirs (str): the folder to save images
    Return:
                transfer (bool): transffering files after render
    '''
        
    render_queue_system = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = render_queue_system.get_queue()

    global NewExecutor
    global image_directories

    image_directories = image_dirs
    unreal.log_warning('Try Cleanup Render folder: '+str(image_directories))
    if os.path.exists(image_directories):
        try:
            shutil.rmtree(image_directories)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (image_directories, e))
        else:
            unreal.log_warning('Cleanup Render folder finished : ' + str(image_directories))

    if not render_queue_system.is_rendering():
        NewExecutor = render_queue_system.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
    else:
        print('Failed start Render. Active executor working on producing a movie: %s' % (image_directories))
        unreal.log_error('Failed start Render. Active executor working on producing a movie: %s' % (image_directories))
        return

    if transfer:
        NewExecutor.on_executor_finished_delegate.add_callable_unique(file_transfer_callback)

    NewExecutor.on_executor_finished_delegate.add_callable_unique(delete_MoviePipelineJob)

    #Check abort and erors during proccess
    NewExecutor.on_executor_errored_delegate.add_callable_unique(errored_MoviePipelineJob)


def delete_MoviePipelineJob(inJob, success):
    print('Delete Queue succes' + str(success))
    print('Delete Queue inJob'+str(inJob))
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = subsystem.get_queue()

    existed_jobs = pipelineQueue.get_jobs()

    print('Delete Queue jobs count= ' + str(len(pipelineQueue.get_jobs())))

    print('Delete jobs image directory : '+image_directories)
    print('Delete jobs job directory : ' + str(inJob))
    unreal.log_warning('Job Render. success :' + str(success))
    for job in existed_jobs:
        outputSetting = job.get_configuration().find_setting_by_class(unreal.MoviePipelineOutputSetting)
        print(outputSetting.output_directory.path)
        if outputSetting.output_directory.path == image_directories:
            pipelineQueue.delete_job(job)
            print('Deleted Finished Job succes : '+job.job_name)
            unreal.log_warning('Job Render. Deleted Finished Job succes :'+job.job_name)
        else:
            unreal.log_warning('Job Render.  Not found Finished Job something going wrong!')

def OpenFolderImages():
    print('Images directories : '+image_directories)
    subprocess.Popen(f'explorer "{image_directories}"')

def get_render_queue_jobs():
    render_queue_system = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    render_queue = render_queue_system.get_queue()
    render_jobs = render_queue.get_jobs()
    return render_jobs

def errored_MoviePipelineJob(Exec, inJob, is_fatal, errortext):
    print('Abort Queue Exec : ' + str(Exec))
    print('Abort Queue inJob : '+str(inJob))
    print('Abort Queue job fatal : ' + str(is_fatal))
    print('Abort Queue job error : ' + str(errortext))
    unreal.log_warning('Job Render. Aborted!')
    delete_MoviePipelineJob(inJob, is_fatal)



