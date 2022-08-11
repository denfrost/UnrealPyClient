import glob
import time
import subprocess
from pathlib import Path
import os
import shutil

import unreal

import utils
import ftp_transfer
#from . import shotgun

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
    
    print('Start Transferring Files ...')

    
    medias = []
    shotgun_media = []
    for dir in image_directories:
    
        image_seq = dir + '\\' + dir.split('_')[-1] + '_SEQ.%04d.exr'
        tl = dir.split('\\')[:-2]
        output_folder = '/'.join(tl) + '/MEDIA'
        folder = Path(output_folder)
        if not folder.exists ():
            os.makedirs(folder)
        
        # make media for shotgun
        output_mov = output_folder + '/' + 'UER_' + dir.split('\\')[-1] + '.mp4'

        #conversion_cmd = f'ffmpeg -y -start_number 101 -i {image_seq} -c:v libx264 -crf 18 -vb 20M -vf fps=25 -pix_fmt yuv420p {output_mov}'
        
        conversion_cmd = f'ffmpeg -y -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -start_number 101 -i {image_seq} -c:v libx264  -vf "lutrgb=r=gammaval(0.416666667):g=gammaval(0.416666667):b=gammaval(0.416666667)" -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -crf 18 -vb 20M {output_mov}'
        
        print (conversion_cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call( conversion_cmd,creationflags=CREATE_NO_WINDOW)


        of = Path(output_mov)
        if of.exists():
            # send media file to L drive
            l_drive_media = ftp_transfer.transfer_data([output_mov])
            
            # publish it to shotgun
            time.sleep(3)
            
            try:
                version = shotgun.publish_shot(dir.split('\\')[-1],l_drive_media[0])
            except:
                print('error in submit to shotgun')

        # transfer rendered frames to Render folder in L
        # duplicate for version first
        
        files_list = []
        files = glob.glob(dir + '/*')
        
        if len(files):
            folder = f'{dir}/V{version}'
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

    
def render_jobs(image_dirs,transfer=False):
    '''
    Render jobs already in render queue

    Parameters:
                image_dirs (str): the folder to save images
    Return:
                transfer (bool): transffering files after render
    '''
        
    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = subsystem.get_queue()

    global NewExecutor
    global image_directories

    image_directories = image_dirs
    
    # cleanup render folder before start rendering
    for d in image_dirs:
        for filename in os.listdir(d):
            file_path = os.path.join(d, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    NewExecutor = subsystem.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
    
    if transfer:
        NewExecutor.on_executor_finished_delegate.add_callable_unique(file_transfer_callback) 
    
   
        
        