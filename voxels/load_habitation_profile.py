import os
import pickle

from oldprofiles.profiles.emptyprofile import EmptyProfile
from oldprofiles.profiles.minecraftfarmvillage import MinecraftFarmVillage
from oldprofiles.profiles.minecraftminingvillage import MinecraftMiningVillage
from oldprofiles.profiles.minecraftmountainvillage import MinecraftMountainVillage

# known_habitation_profiles = {
#             'empty': EmptyProfile,
#             'minecraft_mining_village': EmptyProfile,
#             'minecraft_mountain_village': EmptyProfile,
#             'minecraft_fortified_village': EmptyProfile,
#             'minecraft_water_village': EmptyProfile,
#             'minecraft_farm_village': EmptyProfile,
#         }

known_habitation_profiles = {
            'empty': EmptyProfile,
            'minecraft_mining_village': MinecraftMountainVillage,
            'minecraft_mountain_village': MinecraftMountainVillage,
            'minecraft_fortified_village': MinecraftMountainVillage,
            'minecraft_water_village': MinecraftFarmVillage,
            'minecraft_farm_village': MinecraftFarmVillage,
        }


def load(set_name, save_location, visual_shape, materialization={}):
    if os.path.exists(save_location):
        with open(save_location, "rb") as f:
            return pickle.load(f)
    else:
        print("retrieving habitation profile: " + str(set_name))
        habitation_profile = known_habitation_profiles[set_name](visual_shape, materialization)
        # TODO remove this, for debugging nice to not save
        if False:
            with open(save_location, "wb") as f:
                pickle.dump(habitation_profile, f)
        return habitation_profile
