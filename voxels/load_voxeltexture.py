import os
import pickle

from voxels.cornercity import CornerCity
from voxels.simplecity import SimpleCity

known_sets = {
            'simplecity': SimpleCity,
            'cornercity': CornerCity
        }


def load(set_name, save_location, size):
    if os.path.exists(save_location):
        with open(save_location, "rb") as f:
            return pickle.load(f)
    else:
        set = known_sets[set_name](size)
        with open(save_location, "wb") as f:
            pickle.dump(set, f)
            return set
