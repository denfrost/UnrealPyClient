import glob, os, re

def UtilObserver():
    unreal_source_path = 'C:/WH_KillTeam/UNREAL/SOURCE/ASSETS'
    all_native_assets = glob.glob(unreal_source_path + '/**/FBX/**/*.fbx', recursive=True)
    all_optimized_assets = glob.glob(unreal_source_path + '/**/OPT/**/*.fbx', recursive=True)
    all_assets = all_native_assets
    for index, item in enumerate(all_assets) :
     all_assets[index] = item.replace('\\','/')
    #FBX vs OPT
#Restrict size
    list_of_assets=[]
    for asset in all_assets:
     asset_size = os.stat(asset).st_size / (1000 * 1000)
     if asset_size < 100:
        print(asset + ' --> ' + str(asset_size))
        list_of_assets.append(asset)

#Isolate with a string
#list_of_assets = [x for x in list_of_assets if 'PROPS' in x]


    for index, name in enumerate(list_of_assets):
     #asset_name = name.split('/')[-1].split('.')[0].split('_', 1)[1]
     asset_name = name.split('/')[-1]
     asset_name = name.split('/')[-1].split('.')[0]
     asset_path = "/Game/Assets/StaticMeshes/" + asset_name
     static_mesh_fbx = name
     json_file_path = name.replace('fbx','json')
     asset_size = os.stat(name).st_size / (1000 * 1000)
     print(str(index) + ' --> ' +asset_name + ' --> ' + str(os.stat(name).st_size / (1024 * 1024)).split('.')[0] + ' Mb')

UtilObserver()