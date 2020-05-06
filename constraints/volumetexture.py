import numpy as np
from functools import reduce

from oldprofiles.tiles.tiles import empty_space
from solving.util import is_negative_dimension, dimension_to_number_converter, invert_dimension, rotational_order, \
    get_rotated_dimension, dimension_order_with_negative, sequential_dimension_order, invert_if_negative
from voxels.magicavoxwrapper import visualize_voxel


class VolumeTexture:

    def __init__(self, id, match_volume, visual_volume, categories, direction=None, group=None, overriding_edges={}, route_connections = [], mastergroup=True):
        """
        :param id:
        :param match_volume:
        :param visual_volume:
        :param categories:
        :param direction:
        :param group:
        :param overriding_edges: Overriding edges are written as a dictionary with keys the dimension and as
        value the VolumeTexture that overrides the constraint of this volume texture. So given we have VolumeTexture A, and
        VolumeTexture B. A has overriding edges : {y: B}. This means that the edge y of A, must match with the edge -y of B.
        Therefore the edge y of A will be equal to the edge -y of B.
        """
        self.id = id
        self.group = group if group is not None else id
        self.categories = reduce(lambda agg, e: dict(agg, **{e: True}), categories, {})
        self.direction = direction
        self.visual_volume = VolumeTexture.convert_boolean_array_into_integer_array(visual_volume)
        self.match_volume = match_volume
        self.edges = self.create_constraint_edges()
        self.overriding_edges = overriding_edges
        self.route_connections = route_connections
        self.constraints = {
            "x": {},
            "-x": {},
            "y": {},
            "-y": {},
            "z": {},
            "-z": {}
         }
        self.mastergroup = mastergroup


    @staticmethod
    def convert_boolean_array_into_integer_array(M):
        return M.astype(int)

    # M[x,z,y]
    def create_constraint_edges(self):
        M = self.match_volume
        return {
            "x": M[- 1, :, :],
            "-x": M[0, :, :],
            "z": M[:, :, -1],
            "-z": M[:, :, 0],
            "y": M[:, - 1, :],
            "-y": M[:, 0, :]
         }

    @staticmethod
    def resolve_route_connections(all_route_connections, direction):
        new_all_route_directions = []
        for route_connections in all_route_connections:
            rotated_route_connections = [rotational_order[(rotational_order.index(d) +
                                                          (direction if direction else 0)) % len(rotational_order)]
                                         if d in rotational_order else d
                                         for d in route_connections]
            new_all_route_directions += [rotated_route_connections]
        return new_all_route_directions

    def resolve_overriding_edges(self, textures):
        """
        Resolve here overriding edges by for every overriding edge take that texture and overwrite that edge with
        the known constraint edge. This function has to be run after all the transformed tiles are created, but
        before add_constraints_from_corpus
        :param textures:
        :return:
        """
        textures_dict = reduce(lambda agg, texture: dict(agg, **{texture.id: texture}), textures, {})
        for dim_key in self.overriding_edges:
            accumulated_overriding_texture_edge = None
            # FIXME there is different behavior hardcoded for different dimensions
            # for (-)y overriding edges, different behavior than (-)x, (-)z.
            # This is possible due to it only being interesting rotating tiles over the y axis.
            # But this is not a satisfying implementation at the moment.
            if dim_key in rotational_order:
                rotated_dim = get_rotated_dimension(dim_key, self.direction if self.direction else 0)
                overriding_edge_dim = rotated_dim
            else:
                overriding_edge_dim = dim_key
            overriden_ids = ""
            for edge_override_element in self.overriding_edges[dim_key]:
                overriding_texture_id = edge_override_element
                overriden_ids += overriding_texture_id

                # TODO hack: for now if direction is not found for overriding, take the one
                # without a direction
                overriding_texture = textures_dict[overriding_texture_id] \
                    if overriding_texture_id in textures_dict else textures_dict[overriding_texture_id[:-1]]
                pass

                real_dimension = invert_dimension(overriding_edge_dim) if not overriding_edge_dim in rotational_order else overriding_edge_dim
                accumulated_overriding_texture_edge = \
                    overriding_texture.create_constraint_edges()[real_dimension] \
                        if accumulated_overriding_texture_edge is None \
                    else accumulated_overriding_texture_edge + \
                         overriding_texture.create_constraint_edges()[real_dimension]

            if accumulated_overriding_texture_edge is not None:
                self.edges[overriding_edge_dim] = accumulated_overriding_texture_edge
                # print("for tile: " + self.id + " override on " + overriding_edge_dim + " with "
                #       + overriden_ids)
            else:
                pass

            # print("for tile: " + self.id + " override on " + overriding_edge_dim + " with "
            #       + overriding_texture_id + " from " + invert_dimension(dim_key))


    def add_constraints_from_corpus(self, textures):
        for texture in textures:
            for edge_dim in self.edges:
                current_edge = self.edges[edge_dim]
                if np.alltrue(texture.edges[invert_dimension(edge_dim)] ^ current_edge ^ \
                    np.full(np.shape(current_edge), True)):
                    self.constraints[edge_dim][texture.id] = texture

    def show_constraints(self):
        # self.visualize_edges()
        for constraint in self.constraints:
            if constraint == "x":
                for e in self.constraints[constraint]:
                    switch_places = lambda dimension, A, B: (B, A) if is_negative_dimension(constraint) else (A, B)
                    M = np.concatenate(switch_places(constraint, self.visual_volume, self.constraints[constraint][e].visual_volume),
                                       axis=dimension_to_number_converter(constraint))
                    self.visualize_voxel(M, constraint + "" + e)

                    # M = np.concatenate(switch_places(constraint, self.edges[constraint], self.constraints[constraint][e].edges[invert_dimension(constraint)]),
                    #                    axis=dimension_to_number_converter(constraint))
                    # self.visualize_voxel(M, np.expand_dims(M, axis=2), constraint)

    def visualize_this_voxel(self, name):
        self.visualize_voxel(self.visual_volume, name)

    def visualize_voxel(self, M, name):
        visualize_voxel(M, name)

    def visualize_edges(self):
        for edge_key in self.edges:
            self.visualize_voxel(np.expand_dims(self.edges[edge_key], axis=dimension_to_number_converter(edge_key)), edge_key)

    def merge(self, volume_texture):
        self.id += volume_texture.id
        self.group += volume_texture.group if volume_texture.group is not None else volume_texture.id
        self.categories = dict(self.categories, **reduce(lambda agg, e: dict(agg, **{e: True}), volume_texture.categories, {}))
        self.visual_volume += VolumeTexture.convert_boolean_array_into_integer_array(volume_texture.visual_volume)
        self.match_volume += volume_texture.match_volume
        self.edges = self.create_constraint_edges()
        self.overriding_edges = reduce(lambda agg, key: dict(agg,
                            **{key: (self.overriding_edges[key] if key in self.overriding_edges else []) +
                                    (volume_texture.overriding_edges[key] if key in volume_texture.overriding_edges else [])}),
                                       dimension_order_with_negative, {})
        return self

# def setup(corpus):
#     textures = map(lambda e: VolumeTexture(e.id, e.match_volume, e.visual_volume), corpus)
#     map(lambda texture: texture.add_constraints_from_corpus(textures), textures)
#     return reduce(lambda agg, texture: dict(agg, **{texture.id: texture}), textures, {})


