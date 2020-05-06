import json
import os
import glob

from profileimporter import import_example_as_block, import_profile
from solving.blocksolver import create_block_from_result
from solving.util import dimensional_tuple_to_dict
from voxels.changetiles import change_tiles_in_profile
from voxels.magicavoxwrapper import import_voxel, visualize_voxel
from voxels.voxelstomesh import import_vox_output_mesh, vox_output_mesh

folder = "output"
obj_folder = folder + "obj"

resource_folder = "heuristicrun"# "experimentresults//setupbignew"
cell_size_t = (5,4,5)
CONVERT_MODEL = False
# os.mkdir(obj_folder)

# one folder
# for file in os.listdir(folder):
#     if file.endswith("vox") and not os.path.exists(os.path.join(obj_folder, file + ".obj")):
#         import_vox_output_mesh(os.path.join(folder, file), os.path.join(obj_folder, file + ".obj"))

#recursive



def convert_voxel(model_path):
        with open("../profiles/base/shapebasestairsstreetconstruction.json", 'r') as f:
                profile_json = json.load(f)
        profile = import_profile(profile_json, '5x4x5x', cell_size_t)
        model = import_example_as_block(model_path, cell_size_t, profile, False)
        new_profile = change_tiles_in_profile(profile_json, cell_size_t, '5x4x5xroof')
        model.change_tiles(new_profile)
        return model.show()

for profile_folder in os.listdir(resource_folder):
        profile_folder_path = os.path.join(resource_folder, profile_folder)
        os.path.isdir(profile_folder_path)
        for i, model in enumerate(sorted(os.listdir(profile_folder_path))):
                model_path = os.path.join(profile_folder_path, model)
                os.path.isfile(model_path)
                print(profile_folder + model)
                if CONVERT_MODEL:
                        M = convert_voxel(model_path)
                else:
                        M = import_voxel(model_path)
                # import_vox_output_mesh(model_path, os.path.join(obj_folder, str(profile_folder + model) + ".obj"))
                vox_output_mesh(M, os.path.join(obj_folder, str(profile_folder + model) + ".obj"))



#for i, file in enumerate((f for f in glob.glob(resource_folder + "/*.vox", recursive=True))):
#        import_vox_output_mesh(os.path.join(folder, file), os.path.join(obj_folder, str(i) + ".obj"))
