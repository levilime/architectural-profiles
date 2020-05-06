from constraints.declarativeconstraint import DeclarativeConstraints
from constraints.volumeconstraints import VolumeConstraints
from functools import reduce

from oldprofiles.habitationprofile import HabitationProfile


def profile_merger(name, profiles):
    """
    Merges Habitation profiles that are already instanced.
    :param profiles: Habitation profiles to be merged, that already instantiated.
    :return: new Habitation profile
    """
    combined_tiles = VolumeConstraints(reduce(lambda agg, profile: agg + profile.tiles, profiles, [])).realized_textures
    combined_rules = DeclarativeConstraints(reduce(lambda agg, profile:
                                                   agg + profile.rules.constraints, profiles, []))
    return HabitationProfile(name, combined_tiles, combined_rules)
