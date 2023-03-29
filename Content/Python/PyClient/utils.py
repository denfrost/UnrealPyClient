#
#Thanks AlexQuevillon
#
import os

import unreal


# path: str : Directory path
# return: bool : True if the operation succeeds
def create_directory(path=''):
    return unreal.EditorAssetLibrary.make_directory(directory_path=path)


# from_dir: str : Directory path to duplicate
# to_dir: str : Duplicated directory path
# return: bool : True if the operation succeeds
def duplicate_directory(from_dir='', to_dir=''):
    return unreal.EditorAssetLibrary.duplicate_directory(source_directory_path=from_dir, destination_directory_path=to_dir)


# path: str : Directory path
# return: bool : True if the operation succeeds
def save_directory(path='', force_save=True, recursive=True):
    return unreal.EditorAssetLibrary.save_directory(directory_path=path, only_if_is_dirty=not force_save, recursive=recursive)


# path: str : Directory path
# return: bool : True if the operation succeeds
def delete_directory(path=''):
    return unreal.EditorAssetLibrary.delete_directory(directory_path=path)


# path: str : Directory path
# return: bool : True if the directory exists
def directory_exist(path=''):
    return unreal.EditorAssetLibrary.does_directory_exist(directory_path=path)


# path: str : Directory path
# return: bool : True if the directory exists
def asset_exist(path=''):
    return unreal.EditorAssetLibrary.does_asset_exist(directory_path=path)


# from_dir: str : Directory path to rename
# to_dir: str : Renamed directory path
# return: bool : True if the operation succeeds
def rename_directory(from_dir='', to_dir=''):
    return unreal.EditorAssetLibrary.rename_directory(source_directory_path=from_dir, destination_directory_path=to_dir)


# from_path str : Asset path to duplicate
# to_path: str : Duplicated asset path
# return: bool : True if the operation succeeds
def duplicate_asset(from_path='', to_path=''):
    return unreal.EditorAssetLibrary.duplicate_asset(source_asset_path=from_path, destination_asset_path=to_path)


# path: str : Asset path
# return: bool : True if the operation succeeds
def delete_asset(path=''):
    return unreal.EditorAssetLibrary.delete_asset(asset_path_to_delete=path)


# path: str : Asset path
# return: bool : True if the asset exists
def asset_exist(path=''):
    return unreal.EditorAssetLibrary.does_asset_exist(asset_path=path)

# path: str : Asset path
# return: ue asset
def load_asset(path=''):
    return unreal.EditorAssetLibrary.load_asset(asset_path=path)


# path: str : Asset path
# return: bool : True if the operation succeeds
def save_asset(path='', force_save=True):
    return unreal.EditorAssetLibrary.save_asset(asset_to_save=path, only_if_is_dirty=not force_save)

# from_path: str : Asset path to rename
# to_path: str : Renamed asset path
# return: bool : True if the operation succeeds
def rename_asset(from_path='', to_path=''):
    return unreal.EditorAssetLibrary.rename_asset(source_asset_path=from_path, destination_asset_path=to_path)


# filename: str : Windows file fullname of the asset you want to import
# destination_path: str : Asset path
# option: obj : Import option object. Can be None for assets that does not usually have a pop-up when importing. (e.g. Sound, Texture, etc.)
# return: obj : The import task object
def build_import_task(filename='', destination_name='', destination_path='', options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', destination_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task


# tasks: obj List : The import tasks object. You can get them from buildImportTask()
# return: str List : The paths of successfully imported assets
def execute_import_tasks(tasks=[]):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    imported_asset_paths = []
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            imported_asset_paths.append(path)
    return imported_asset_paths


# return: obj : Import option object. The basic import options for importing a static mesh
def build_staticmesh_import_options():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', False)  # Static Mesh
    # unreal.FbxMeshImportData
    options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    normalImport = unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
    options.static_mesh_import_data.set_editor_property('normal_import_method', normalImport)
    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', False)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
    # Nanite
    #options.static_mesh_import_data.set_editor_property('build_nanite', True)
    return options


# return: obj : Import option object. The basic import options for importing a skeletal mesh
def build_skeletalmesh_import_options(skeleton_path=''):
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', True)  # Skeletal Mesh
    if not skeleton_path=='':
        options.skeleton = unreal.load_asset(skeleton_path)
    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    options.skeletal_mesh_import_data.set_editor_property('import_meshes_in_bone_hierarchy', True)
    return options


# skeleton_path: str : Skeleton asset path of the skeleton that will be used to bind the animation
# return: obj : Import option object. The basic import options for importing an animation
def build_animation_import_options(skeleton_path=''):
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_animations', True)
    options.set_editor_property('import_mesh', False)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('create_physics_asset', False)
    options.skeleton = unreal.load_asset(skeleton_path)
    # unreal.FbxMeshImportData
    options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxAnimSequenceImportData
    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    return options


def alembic_import_options_skeleton(abc_path=''):
    options = unreal.AbcImportSettings()
    options.set_editor_property('import_type', unreal.AlembicImportType.SKELETAL)
    options.set_editor_property('normal_generation_settings', unreal.AbcNormalGenerationSettings(force_one_smoothing_group_per_object=True))
    options.set_editor_property('conversion_settings', unreal.AbcConversionSettings(rotation=[90.0, 0.0, 0.0]))
    options.set_editor_property('material_settings', unreal.AbcMaterialSettings(create_materials=True))
    return options


def alembic_import_options_geocache(abc_path=''):
    options = unreal.AbcImportSettings()
    options.set_editor_property('import_type', unreal.AlembicImportType.GEOMETRY_CACHE)
    options.set_editor_property('conversion_settings', unreal.AbcConversionSettings(rotation=[90.0, 0.0, 0.0]))
    options.set_editor_property('geometry_cache_settings', unreal.AbcGeometryCacheSettings(motion_vectors=unreal.AbcGeometryCacheMotionVectorsImport.IMPORT_ABC_VELOCITIES_AS_MOTION_VECTORS))
    options.set_editor_property('material_settings', unreal.AbcMaterialSettings(create_materials=True))
    return options


#Return true if there is a second texture to form a sequence aka it's a UDIM
def checkifudim(texturefile):
    if '1001' in texturefile:
        return os.path.isfile(texturefile.replace('1001','1002'))


def get_moviequeue_jobs_list():

    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipelineQueue = subsystem.get_queue()
    return pipelineQueue.get_jobs()

def list_presets_rendering():
    #Create list of presets rendering
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path('/Game/Cinematics/MoviePipeline/Presets', recursive=True)
    list_presets = []
    for asset in assets:
        print(asset.asset_class)
        if (asset.asset_class == 'MoviePipelineMasterConfig'):
            list_presets.append(asset)
    return list_presets

def list_skel_meshes():
    #Create list of skeletal meshes
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path('/Game/ASSETS/SKELETAL', recursive=True)
    skeletal_assets = []
    for asset in assets:
        if asset.asset_class == 'SkeletalMesh':
            skeletal_assets.append(asset)
    return skeletal_assets

def list_grooms_assetbypath(assetpath, recursive=False):
    #Create list of Groom
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path(assetpath, recursive)
    groom_assets = []
    for asset in assets:
        if asset.asset_class == 'GroomAsset':
            groom_assets.append(asset)
    return groom_assets

def list_groom_binding_assetbypath(assetpath, recursive=False):
    #Create list of Bindings
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path(assetpath, recursive)
    groom_assets = []
    for asset in assets:
        if asset.asset_class == 'GroomBindingAsset':
            groom_assets.append(asset)
    return groom_assets


def list_grooms_asset():
    #Create list of Groom
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path('/Game/ASSETS/SKELETAL', recursive=True)
    groom_assets = []
    for asset in assets:
        if asset.asset_class == 'GroomAsset':
            groom_assets.append(asset)
    return groom_assets

def list_groom_binding_asset():
    #Create list of Bindings
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path('/Game/ASSETS/SKELETAL', recursive=True)
    groom_assets = []
    for asset in assets:
        if asset.asset_class == 'GroomBindingAsset':
            groom_assets.append(asset)
    return groom_assets

def list_groomcaches():
    #Create list of Groom
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path('/Game/ASSETS/SKELETAL', recursive=True)
    groomcache_assets = []
    for asset in assets:
        if asset.asset_class == 'GroomCache':
            groomcache_assets.append(asset)
    return groomcache_assets
