from functools import reduce
from itertools import product

import numpy as np

from solving.blocksolver import create_block_from_voxels
from solving.util import merge_dicts, get_adjacent_indices, is_in_range, invert_dimension, dimension_index_values
from voxels.magicavoxwrapper import import_voxel


def semantic_voxels_to_mesh(M, cell_size, profile):
    block = create_block_from_voxels(M, cell_size, profile)
    M = np.rot90(M, 2, (0, 1))
    def direction_is_closed(type, cell, d):
        if d not in cell.neighbors:
            return False
        t = cell.neighbors[d].get_tile_in_contains()
        tile = t["tile"]
        rotY = t["rotY"]
        return invert_dimension(d) in tile.get_adjacencies_with_directions(type, rotY, entrance=False)

    open_cell_directions = {}
    for cell in block.cells:
        t = cell.get_tile_in_contains()
        tile = t["tile"]
        rotY = t["rotY"]
        open_directions = reduce(lambda ds, type:
                                 ds.union(
                                     [d for d in tile.get_adjacencies_with_directions(type, rotY, entrance=False)
                                      if not direction_is_closed(type, cell, d)]
                                 ),
               tile.available_types(), set())
        open_cell_directions[cell.id] = open_directions

    # color all voxels that need it because they coincide with an open cell
    color_match = Color_Match(open_cell_directions, cell_size)
    return voxels_to_mesh(M, color_match)

class Color_Match:

    def __init__(self, open_cell_directions, cell_size):
        matches = set()
        for cell_index in open_cell_directions:
            for d in open_cell_directions[cell_index]:
                matches.add((*cell_index, *dimension_index_values[d]))
        self.matches = matches
        self.cell_size = cell_size

    def __contains__(self, location):
        """
        :param location: (x,y,z,dimension index, dimension direction), where x,y,z a voxel index
        :return:
        """
        position = location[:3]
        i = location[3]
        if location[i] + max(location[i], 0) % self.cell_size[i]:
            return False
        cell_position = tuple(np.floor_divide(position, self.cell_size))
        return (*cell_position, *location[3:5]) in self.matches


def voxels_to_mesh(M, cutoff_face=set()):
    """
    creates a naive mesh from voxels. The focus is on only creating polygons at the boundaries
    between valued voxels and empty voxels. This method doesn't use marching cubes, but keeps
    the cubeness of the voxles fully intact.
    :param M:
    :return:
    """
    all_vertices = list(product(*[range(0, x + 1) for x in M.shape]))
    # create vertice keys with as value the index, obj index starts at 1
    vertices = reduce(lambda points, t: merge_dicts(points, {t[1]: t[0] + 1}),
                      enumerate(all_vertices), {})
    found_faces = []
    cut_faces = []

    it = np.nditer(M, flags=['multi_index'])

    def get_face_triangle(vertice_coords):
        return [vertices[c] for c in vertice_coords]

    def get_square_face(vertice_coords):
        # return [get_face_triangle(vertice_coords)]
        return [list(reversed(get_face_triangle(vertice_coords[0:3]))), get_face_triangle(vertice_coords[1:4])]

    # go over all voxels
    while not it.finished:
        index = it.multi_index
        current_color = M[index]
        # if the voxel is empty than ignore it
        if is_empty(current_color):
            it.iternext()
            continue

        # get adjacent voxel positions
        adjacencies = get_adjacent_indices(index)
        # go over all adjacent voxel positions
        for p in adjacencies:
            # if the position is within the range of the total shape and the position is not an empty voxel
            if not is_in_range(p, (0, 0, 0), M.shape) or is_empty(M[p[0], p[1], p[2]]):
                # direction of this position vs the current position
                relative_difference = np.subtract(p, index)
                # static index contains the index that is changed in the adjacent position compared with the current
                static_index = list(filter(lambda t: t[1] != 0, enumerate(relative_difference)))[0][0]
                # up_down_position whether it is above or below in the dimension corresponding with static index
                up_down_position = 1 if np.sum(relative_difference) > 0 else 0
                relevant_vertices = list(product(*[[index[i] + up_down_position] if i == static_index else
                                                   [index[i], index[i] + 1] for i in range(0, len(M.shape))]))
                faces = get_square_face(relevant_vertices)
                if static_index == 1 and np.sum(relative_difference) > 0:
                    faces = [list(reversed(face)) for face in faces]
                elif np.sum(relative_difference) < 0 and not static_index == 1:
                    faces = [list(reversed(face)) for face in faces]
                if (*index, static_index, up_down_position) in cutoff_face:
                    cut_faces.extend(faces)
                else:
                    found_faces.extend(faces)
        it.iternext()

    return all_vertices, found_faces, cut_faces


def create_obj(M, save_location):
    f = open(save_location, "w+")
    vertices, faces, cut_faces = voxels_to_mesh(M)
    for vertice in vertices:
        f.write(f"v {' '.join(map(str, vertice))}\n")
    for face in faces:
        f.write(f"f {' '.join(map(str, face))}\n")
    f.close()


def semantic_create_obj(M, profile, cell_size, save_location):
    f = open(save_location + ".obj", "w+")
    f.write(f"mtllib {save_location}.mtl\n")
    vertices, faces, cut_faces = semantic_voxels_to_mesh(M, cell_size, profile)
    for vertice in vertices:
        f.write(f"v {' '.join(map(str, vertice))}\n")
    #f.write(f"usemtl Default\n")
    for face in faces:
        f.write(f"f {' '.join(map(str, face))}\n")
    f.write(f"usemtl cs\n")
    for face in cut_faces:
        f.write(f"f {' '.join(map(str, face))}\n")
    f.close()

    f = open(save_location + ".mtl", "w+")

    f.write(f"newmtl cs\n"
            f"Ka 0.000000 0.000000 0.000000\n"
            f"Kd 0.000000 0.000000 0.000000\n"
            f"Ks 0.000000 0.000000 0.000000\n"
            f"Ns 0.000000\n")
    f.close()




def is_empty(number):
    return number == 0


def import_vox_output_mesh(path, save_location):
    M = import_voxel(path)
    M = np.rot90(M, 2, (0, 1))
    create_obj(M, save_location)

def vox_output_mesh(model, save_location):
    create_obj(np.rot90(model, 2, (0, 1)), save_location)


# M = import_voxel('flathouses/result0.vox')
#
# # M = np.full((2,2,2), 1)
# # M[1,0,1] = 0
# # M[0,1,0] = 0
# # M[1,1,0] = 0
# # M[0,1,1] = 0
#
# with open("profiles/base.json", 'r') as f:
#     profile_json = json.load(f)
#
# cell_size = (5, 4, 5)
#
# profile = import_profile(profile_json, '5x4x5x', cell_size)
# # M = np.rot90(M, 2, (0,1))
# # semantic_create_obj(M, profile, cell_size, "cool")
#
# create_obj(M, "cool.obj")