import os
from ftplib import FTP
import ftplib
import base64
#from base64 import b64decode as memeIt

from . import config


ROOT = '/ifs/data/picturethis/Projects/'


def memeIt(s):
    '''
    decrypting the encrypted conneting data

    Parameters:
                s (str): string to be decrypted
    Return:
                decrypted string
       
    '''
    
    return base64.b64decode(s.encode()).decode()
    
def translate_path(path):
    '''
    Transalting a windows path in L: to ftp path

    Parameters:
                path (str): the path of file or folder in L:
    Return:
                translated_path (str): translated ftp path
    '''
     
    if 'L:/' in path:
        translated_path = path.replace('L:/', '%s/LIVE/' % ROOT)

    if '/LIVE/' in path:
        translated_path = '%s/LIVE/%s' % (ROOT, path.split('/LIVE/')[-1])

    translated_path = translated_path.replace('///', '/')
    translated_path = translated_path.replace('//','/')

    return translated_path


def connect_ftp():
    
    '''
    Connecting to ftp service 

    
    Return:
            ftp (FTP): handle of ftp service
    
    '''
    
    ftp = FTP(host=memeIt("aXNpbG9uLW1nLmFkLnBpY3R1cmV0aGlzYW5pbWF0aW9uLmNvbQ=="))

    print(ftp.getwelcome())

    # Login to the FTP server
    ftpResponse = ftp.login(user=memeIt("UElDVFVSRVRISVNcbWVtZQ=="), passwd=memeIt("TGV0c1RAa2UhdA=="))
    print(ftpResponse)
   
    return ftp


def cd_tree(currentDir,ftp_cnt):
    '''
    Create directories recursively in ftp 

    Parameters:
                currentDir (str): the path of folder to be created
                ftp_cnt (FTP): ftp handle
    
    '''
       
    if currentDir != "":
        try:
            ftp_cnt.cwd(currentDir)
        except ftplib.error_perm:
            
            cd_tree("/".join(currentDir.split("/")[:-1]) ,ftp_cnt)
            ftp_cnt.mkd(currentDir)
            ftp_cnt.cwd(currentDir)



def make_directories(dirpath,ftp_cnt):
    '''
    make dirctoried for rendered files in L

    Parameters:
                dirpath (str): directory or file address
                ftp_cnt (FTP): ftp handle
    Return:
                dirpath (str): list of directories has been created 
    '''
    
    if ('.' in dirpath):
        dirpath = os.path.dirname(dirpath)

    #print(dirpath +'\n')
        
    if not os.path.exists(dirpath):
        
        dirpath = dirpath.replace('\\', '/')
        
        t_path = translate_path(dirpath)
        
        cd_tree(t_path,ftp_cnt)
       

    return dirpath

def quit(ftp_cnt):
    '''
    close the ftp connection

    Parameters:
                ftp_cnt (FTP): ftp handle
   
    '''
    
    try:
        ftp_cnt.quit()
        connect = None
    except:
        pass


def transfer_data(data):
    '''
    transfer files to proper address using ftp

    Parameters:
                data (list): list of files in local machine to be transferd
                
    Return:
                destination (list): list of files in server
    '''
    
    ftp_hndl = connect_ftp()
    print('---------TRANSFERRING OF FILES STARTED---------\n\n')
    destination = []
    for path in data:
        path = path.replace('\\', '/')
        
        server_path = config.source_drive + path.split('/LIVE/')[-1]
        print('server_path :'+server_path)
        destination.append(server_path)
        
        dir_path = make_directories(server_path,ftp_hndl)
        #print(dir_path)
        # remove server file first, then upload new
        
        ftp_server_path = translate_path(server_path)
        
        if os.path.exists(server_path):
            ftp_hndl.delete(ftp_server_path)
        
        # transferring
        
        with open(path, "rb") as fileObject:
            ftp_hndl.storbinary('STOR ' + ftp_server_path, fileObject)
        print( f'transferring {path} done\n')

    
    quit(ftp_hndl)
    print('---------TRANSFERRING OF FILES FINISHED---------\n\n')

    return destination

