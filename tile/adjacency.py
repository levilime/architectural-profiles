from functools import reduce

from solving.util import deep_merge, invert_dimension, rotational_order, get_rotated_dimension, merge_dicts, \
    objects_with_id_field_to_dict
import numpy as np

class Adjacencies:

    def __init__(self, tiles, directions, serialized_adjacencies, empty_tile_id):
        tiles_dict = reduce(lambda agg, tile: merge_dicts(agg, {tile.id: tile}), tiles, {})
        self.directions = directions
        self.adjacency_per_tile_dict = {}
        self.empty_tile = tiles_dict[empty_tile_id]
        self_adjacencies = {}
        complete_match_adjacencies = {}

        for tile in filter(lambda tile: tile.id in serialized_adjacencies["strict_adjacency"].get("self", []), tiles):
            self_adjacencies[tile.id] = self.resolve_self_adjacency(tile)
        for complete_match in serialized_adjacencies["strict_adjacency"].get("complete_match", []):
            complete_match_adjacencies = deep_merge(complete_match_adjacencies,
                                                    self.match_tiles_on_all_directions(
                list(map(lambda k: tiles_dict[k], complete_match))))
        explicit_adjacencies = self.consume_adjacencies(tiles_dict, serialized_adjacencies["strict_adjacency"].get("edges", []))

        all_adjacencies = reduce(deep_merge, [self_adjacencies, complete_match_adjacencies, explicit_adjacencies])

        self.strict_adjacencies = all_adjacencies
        # self.routing_adjacencies = routing_adjacencies

    def resolve_self_adjacency(self, tile):
        self_adjacency = \
            reduce(lambda agg, d: deep_merge(agg, {d: add_addjacency(tile)}), self.directions,
                   {})
        return self_adjacency

    def match_tiles_on_all_directions(self, tiles):
        adjacencies = {}
        for current_tile in tiles:
            for other_tile in filter(lambda tile: not tile.equal(current_tile), tiles):
                adjacencies = deep_merge(adjacencies, {current_tile.id:
                                                           reduce(lambda agg, d:
                                                                            dict(agg,
                                                                                 **{d: add_addjacency(other_tile)}),
                                                                            self.directions, {})
                                                       })
        return adjacencies

    def consume_adjacencies(self, tiles, adjacencies):
        new_adjacencies = {}
        for adjacency in adjacencies:
            left = adjacency[0]
            right = adjacency[1]
            new_adjacencies = deep_merge(new_adjacencies, add_addjacencies(tiles[left["id"]],
                             tiles[right["id"]],
                             left["rotY"],
                             left["dir"],
                             right["rotY"],
                             right["dir"]))
        return new_adjacencies

    @staticmethod
    def consume_subset_adjacencies(subset_adjacencies, general_adjacencies):
        new_adjacencies = {}
        subset_adjacencies_d = reduce(lambda agg, e: dict(agg, **{e["id"]: e['paths']}), subset_adjacencies, {})
        for routing_adjacency in subset_adjacencies:
            id = routing_adjacency["id"]
            if id not in general_adjacencies:
                print(f"tile {id} did not occur in adjacencies found in the examples")
                continue
            routes = routing_adjacency["paths"]
            # do rotation to stand before tile correctly that might be rotated in example
            if len(list(filter(lambda k: k not in general_adjacencies[id], routes))) > 0:
                print(id + " not all subset has an adjacency.")
            # FIXME may not include rotations in general adjacencies that have no subset part
            # for example adjacency(routing,flatsurface,stairs,x,0,1,0) is ok, but not adjacency(routing,flatsurface,stairs,x,0,0,0)
            added_adjacencies = {}
            for d in routes:
                ll = []
                if d not in general_adjacencies[id]:
                    print(f"tile {id} does not have adjacencies for direction {d}")
                    continue
                for other_side_adjacency in general_adjacencies[id][d]:
                    rotated_other_side_dim = get_rotated_dimension(invert_dimension(d), 4 - other_side_adjacency[2])
                    if other_side_adjacency[0] in subset_adjacencies_d and \
                            rotated_other_side_dim in subset_adjacencies_d[other_side_adjacency[0]]:
                        ll.append(other_side_adjacency)
                added_adjacencies[d] = ll
            new_adjacencies[id] = added_adjacencies
            # new_adjacencies[id] = reduce(lambda agg, d: dict(agg, **{d: general_adjacencies[id][d]}), routes, {})
            #new_adjacencies[id] = reduce(lambda agg, d: dict(agg, **{d:
            #                      Adjacencies.choose_all_that_connect(
            #.                      general_adjacencies, id, d, subset_adjacencies_d)}), routes, {})
        return new_adjacencies

    @staticmethod
    def choose_all_that_connect(general_adjacencies, tile_id, direction, subset_adjacencies_d):
        def existing_dimensions(dimensions, rotation):
            return [get_rotated_dimension(d, rotation) for d in dimensions]
        chosen_adjacencies = [adjacency for adjacency in general_adjacencies[tile_id][direction]
         if adjacency[0] in subset_adjacencies_d and
         # the adjacent tile needs to also point to the tile in the opposite direction
         invert_dimension(direction) in existing_dimensions(subset_adjacencies_d[adjacency[0]], adjacency[2])]
        pruned_adjacencies = {}
        for adjacency in chosen_adjacencies:
            pruned_adjacencies[adjacency] = general_adjacencies[tile_id][direction][adjacency]
        return pruned_adjacencies


def adjacency_two_tiles(profile, tile_a, tile_b, direction, adjacency_subset=None):
    rotated_dimension = get_rotated_dimension(direction, int(4 - tile_a[2]))
    rotated_tile_b_without_mod = (tile_b[0], *np.subtract(list(map(int, tile_b[1:])), list(map(int, (tile_a[1:])))).tolist())
    rotated_tile_b = (tile_b[0], *map(lambda x: x % 4, rotated_tile_b_without_mod[1:]))
    # rotated_tile_b_in_str = (rotated_tile_b[0], *[str(x) for x in rotated_tile_b][1:])
    relevant_adjacencies = profile.additional_adjacencies[adjacency_subset] if adjacency_subset else profile.adjacencies
    is_connected = rotated_dimension in relevant_adjacencies[tile_a[0]] and rotated_tile_b in \
           relevant_adjacencies[tile_a[0]][rotated_dimension]
    # print(tile_a, tile_b, direction, adjacency_subset,  is_connected)
    return is_connected

class Adjacency:

    def __init__(self, tile, rotY=0, rotX=0, rotZ=0):
        self.tile = tile
        self.rotX = rotX
        self.rotZ = rotZ
        self.rotY = rotY


# def add_addjacency(from_tile, from_rotY, to_id, to_dir):
#     elem = Adjacency(from_tile, int(from_rotY))
#     return {to_id: {to_dir: [elem]}}


def add_addjacency(tile, rotY=0, from_rot_y=0):
    adjusted_rot = int((rotY - from_rot_y) % len(rotational_order))
    return {(tile.id, 0, adjusted_rot , 0): Adjacency(tile, adjusted_rot)}


def add_addjacencies(from_tile, to_tile, from_rotY, from_dir, to_rotY, to_dir):
    rotated_dim = list(reversed(rotational_order))[(list(reversed(rotational_order)).index(from_dir) + from_rotY) % len(rotational_order)] \
        if from_dir in rotational_order else from_dir
    return {from_tile.id: {rotated_dim: add_addjacency(to_tile, to_rotY, from_rotY)}}
             #         {to_tile.id: {to_dir:add_addjacency(from_tile, from_rotY, to_rotY)}})


def adjacencies_tile_according_to_subject(serialized_adjacencies, subject):
    d = dict()
    for adjacency_key in [x for x in serialized_adjacencies if not x == "strict_adjacency"]:
        adjacencies = serialized_adjacencies[adjacency_key]
        for adjacency in adjacencies:
            d = deep_merge(d, {
                adjacency["id"]: {
                    adjacency_key: adjacency[subject] if subject in adjacency else []
                }
            })
    return d


def adjacencies_tile_ordered(serialized_adjacencies):
    return adjacencies_tile_according_to_subject(serialized_adjacencies, "paths")


def get_entrance_adjacencies(serialized_adjacencies):
    return adjacencies_tile_according_to_subject(serialized_adjacencies, "entrance")
