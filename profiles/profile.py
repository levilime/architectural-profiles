import json

from solving.util import merge_dicts
import copy

class Profile:

    def __init__(
            self,
            tiles,
            adjacencies,
            connectivities,
            all_connected,
            blobs,
            blobs_to_side,
            connected_through,
            empty_tile, additional_adjacencies={},
            hard_override=False,
            cut_off=[],
            density={},
            shapes=[],
            shape_adjacencies=[],
            purposeful_shape_connections=[]):
        self.tiles = tiles
        self.adjacencies = adjacencies
        self.connectivities = connectivities
        self.all_connected = all_connected
        self.connectivity_blobs = blobs
        self.empty_tile = empty_tile
        self.rules = None
        self.additional_adjacencies = additional_adjacencies
        self.hard_override = hard_override
        self.connected_through = connected_through
        self.cut_off = cut_off
        self.density = density
        self.blobs_to_side = blobs_to_side
        self.shapes = shapes
        self.shape_adjacencies = shape_adjacencies
        self.purposeful_shape_connections = purposeful_shape_connections
        # if active shapes is None than all shapes are active, otherwise only
        # the shapes that coincide with the shape names defined in active shapes are active.
        self.active_shapes = None

    def get_all_adjacencies(self):
        return merge_dicts({"strict": self.adjacencies}, self.additional_adjacencies)

    def copy_profile_other_tiles(self, tiles, empty_tile):
        new_profile = copy.copy(self)
        new_profile.tiles = tiles
        new_profile.empty_tile = empty_tile
        return new_profile

    def copy_profile(self):
        return self.copy_profile_other_tiles(self.tiles, self.empty_tile)

    def remove_all_adjancies_tile(self, id):
        for tile_id in self.adjacencies:
            for direction in self.adjacencies[tile_id]:
                if tile_id == id:
                    self.adjacencies[tile_id][direction] = set()
                else:
                    self.adjacencies[tile_id][direction] = set([t for t in self.adjacencies[tile_id][direction] if not t[0] == id])

    #TODO NOT UPDATED
    def get_profile_json(self):
        return {
            "tiles": json.dumps([self.tiles[tile].serialize() for tile in self.tiles]),
            "adjacencies": json.dumps(self.get_all_adjacencies()),
            "connectivities": json.dumps(self.connectivities),
            "allconnected": json.dumps(self.all_connected),
            "blobs": json.dumps(self.connectivity_blobs),
            "cutoff": json.dumps(self.cut_off),
            "density": json.dumps(self.density),
            "empty_tile": self.empty_tile.id
        }
