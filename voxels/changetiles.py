from run_utils.profileimporter import get_tiles, import_profile


def change_tiles_in_profile(profile_json, cell_size_t, other_tile_set):
    profile = import_profile(profile_json, '5x4x5x', cell_size_t)
    new_tiles = get_tiles(profile_json, other_tile_set)
    # change tileset
    for k in profile.tiles:
        profile.tiles[k].shape = new_tiles[k].shape
    return profile