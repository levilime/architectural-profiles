import json

from oldprofiles.util import fill_diagonally_upwards, fill_all, fill_block_floor
from profileimporter import import_profile
from habitationresolver import habitation_resolver
from reflectexample import reflects_examples
from solving.util import dimensional_dict_to_tuple
from voxels.magicavoxwrapper import visualize_voxel


cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x":2, "y":1, "z":2}

with open("profiles/corner.json", 'r') as f:
    profile_json = json.load(f)

profile = import_profile(profile_json, '5x4x5x', (5,4,5))
assert(reflects_examples(profile, profile_json, '5x4x5x', block_size, cell_size))

result = habitation_resolver(profile, block_size, cell_size, [(0,0,0)],
                             {
                                 (0,0,0):
                                  {"filled_assignment":
                                       fill_all(dimensional_dict_to_tuple(block_size))
                                   }},
                             #     (0, 0, 1):
                             #         {"filled_assignment":
                             #           fill_block_floor((5, 5, 5))
                             #          }
                             # }

                             #{}
                             )
visualize_voxel(result)
