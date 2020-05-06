from functools import reduce
import math
from PIL import Image
import numpy as np

from run_utils.adjacencyfromexample import all_tiles_at_postions
from clingo.aspresult import SOLUTION_ID_TOKEN, Solution, SHAPE_PLACEMENT_ANNOTATION
from profiles.profile import Profile
from .cell import Cell
from .util import create_grid, get_filled_array_from_starting_block, dimension_order, dimensional_dict_to_tuple, \
    objects_with_id_field_to_dict, merge_dicts, breadth_first_search_for_graph, dimensional_tuple_to_dict, min_of_list, max_of_list


class BlockSolver:
    """
    Controls cells
    """
    @staticmethod
    def reverse_map(dimension):
        return {
        "x": "-x",
        "-x": "x",
        "y": "-y",
        "-y": "y",
        "z": "-z",
        "-z": "z"
    }[dimension]

    @staticmethod
    def weird_reverse_map(dimension):
        return {
        "x": "-x",
        "-x": "x",
        "y": "y",
        "-y": "-y",
        "z": "-z",
        "-z": "z"
    }[dimension]

    # blocks may not be empty
    def __init__(self, block_size, cell_size, profile, edge_constraints={}, void=False, expanded_boundaries={}):
        # total amount of pixels in all dimensions of the block.
        self.successful = None
        self.block_size = block_size
        self.void = void
        self.profile = profile
        # size of one cell in amount of pixels.
        self.cell_size = cell_size
        block_shape = reduce(lambda agg, dim_key: dict(agg, **{dim_key: math.floor(self.block_size[dim_key])}),
                             self.block_size, {})
        # dimensions of the grid of blocks, the amount of blocks in every dimension.
        self.block_shape = block_shape
        self.reset_cells()
        creation_function = lambda i: Cell(list(profile.tiles.values()), i, self.cell_size)
        self.cells = create_grid(block_shape, creation_function)
        self.cells_d = self.get_cells_dict()
        self.constrained_cells = {}
        self.expanded_boundaries = expanded_boundaries
        self.solved_neighbors = edge_constraints

    def get_cell_according_to_index(self, index):
        return list(filter(lambda cell: cell.id == tuple(index), self.cells))[0]

    def is_succesful(self):
        self.successful = True

    def reset_cells(self):
        creation_function = lambda i: Cell(list(self.profile.tiles.values()), i, self.cell_size)
        self.cells = create_grid(self.block_shape, creation_function)

    def error_block_img(self):
        return Image.new('RGB', (self.cell_size['x'], self.cell_size['y']), color=(255, 0, 0))

    def error_block_voxel(self):
        print("error block")
        return np.full(tuple(map(lambda key: self.cell_size[key], dimension_order)), False)

    def show(self):
        if len(list(self.cell_size)) == 2:
            return self.show_img()
        elif len(list(self.cell_size)) == 3:
            return self.show_voxels()
        else:
            print("only implemented showing something that is 2 or 3 dimensional.")

    def set_cells(self, cells):
        self.cells = cells
        self.cells_d = self.get_cells_dict()

    def show_voxels(self, method=lambda x, rotations: x.show_with_rotation(rotations)):
        if len(self.cells) < 1:
            raise ValueError('Cells are empty. They cannot be displayed')
        # copy the cells
        start_cell = self.cells[0].copy()
        return get_filled_array_from_starting_block(start_cell, len(self.block_size),
                                                    lambda cell: method(list(cell.contains.values())[0],
                                                                        list(cell.contains)[0][1:]) if len(cell.contains) == 1 else
                                                    self.empty_tile()
                                                    #if True or len(cell.contains) > 0 and len(choose_conforming_to_neighbors(cell)) > 0
                                                    #else self.error_block_voxel()
                                                    , "cell")

    def change_tiles(self, new_profile):
        """exploits impurity to change the tiles in the cells"""
        for i in self.cells_d:
            current_tile = self.cells_d[i].get_tile_in_contains()
            self.cells_d[i].set_tile(new_profile.tiles[current_tile["tile"].id], current_tile["rotY"])


    def empty_tile(self):
        tile = np.full(dimensional_dict_to_tuple(self.cell_size), 0)
        # FIXME add line below again
        tile[tuple(map(lambda x: int(x/2), tile.shape))] = 1
        return tile

    def show_adjacency(self, type):
        return self.show_voxels(lambda x, rotations: x.show_adjacency_with_rotation(type, rotations))

    def show_different_color_per_tile(self, colormap):
        return self.show_voxels(lambda x, rotations: x.show_with_rotation(rotations).astype(bool).astype(int) * colormap[x.id])

    def show_img(self):
        img = Image.new('RGB', (self.block_size['x'] * self.cell_size['x'],
                                self.block_size['y'] * self.cell_size['y']), color=(255, 255, 255))
        for i, cell in enumerate(self.cells):
            values = list(cell.contains.values())
            chosen_val = cell.show_possibilities() if len(values) >= 1 else self.error_block_img()
            coord = ((i % self.block_shape['x']) * self.cell_size["x"],
                     math.floor(i / self.block_shape['x']) * self.cell_size["y"])
            img.paste(
                chosen_val
                , (coord[0], coord[1], coord[0] + self.cell_size["x"], coord[1] + self.cell_size["y"]))
        return img

    def get_cells_dict(self):
        return objects_with_id_field_to_dict(self.cells)

    def get_shapes_in_block(self):
        cells_d = self.cells_d

        covered = set()
        def direction_f(position):
            cell = cells_d[position]
            t = cell.get_tile_in_contains()
            tile = t["tile"]
            rotY = t["rotY"]
            traversable_directions = reduce(lambda agg, t:
                                            agg.union(tile.get_adjacencies_with_directions(
                                                t, rotY)),
                                            tile.adjacencies, set())
            return [cell.neighbors[direction].id for direction in traversable_directions
                    if direction in cell.neighbors and cell.neighbors[direction].id not in covered]
        shapes_cells = []
        for cell in self.cells:
            if cell.id not in covered:
                positions = breadth_first_search_for_graph(cell.id,
                                               lambda x: True,
                                               direction_f)
                covered = covered.union(positions)
                shapes_cells.append([cells_d[position] for position in positions])
        return shapes_cells




def get_block_signature(self):
    """
    Block signature is given as {position: (TileID, RotX, RotY, RotZ)}
    :param self:
    :return: Block signature is given as {position: (TileID, RotX, RotY, RotZ)}
    """
    return reduce(lambda agg, cell: merge_dicts(agg,
                                                {cell.id: (cell.get_tile_in_contains()[0],
                                                           0, cell.get_tile_in_contains()[1], 0)}),
                  self.cells, {})


def create_block_from_voxels(voxels, cell_size_t: tuple, profile, tile_exemption_allowed=False):
    block_size_t = tuple(map(int, np.divide(voxels.shape, cell_size_t)))
    tiles_at_position = all_tiles_at_postions(voxels, cell_size_t, profile.tiles, tile_exemption_allowed)
    block = BlockSolver(dimensional_tuple_to_dict(block_size_t), dimensional_tuple_to_dict(cell_size_t), profile)
    for cell in block.cells:
        tile = tiles_at_position[cell.id]
        cell.set_tile(tile["tile"], tile["rotY"])
    return block


def create_block_from_result(solution: Solution, profile: Profile, cell_size):
    block_size, minimum_position = solution.represented_block_size()
    block_objective = BlockSolver(block_size, cell_size, profile)
    return block_from_result(solution, block_objective)




def block_from_cells(cells, profile, cell_size):
    ids = [cell.id for cell in cells]
    mi = min_of_list(ids)
    ma = max_of_list(ids)
    dist_from_origin = np.subtract(ma, mi)
    block_size_t = tuple(map(int, np.add(dist_from_origin, 1)))
    # if np.product(block_size) != len(cells):
    #     raise ValueError(f"{str(block_size)} not completely filled by {len(cells)} cells. "
    #                      f"Cells can only form a block if it is a filled cuboid")
    block = BlockSolver(dimensional_tuple_to_dict(block_size_t), cell_size, profile)
    new_origin_cells = []
    for cell in cells:
        new_cell = Cell([],
                        tuple(np.subtract(cell.id, mi)),
                        cell.cell_size)
        # make a copy of the contains
        new_cell.contains = merge_dicts(cell.contains, {})
        new_origin_cells.append(new_cell)
    block.set_cells(new_origin_cells)
    return block


def block_from_result(solution, block_objective,
                       block_objective_index=(0, 0, 0)):
    block_size = dimensional_dict_to_tuple(block_objective.block_size)
    i = 0
    clingo_computed_cells = solution.values
    computed_cells = map(lambda cell: (cell["x"], cell["y"], cell["z"], cell[SOLUTION_ID_TOKEN],
                                       cell["rx"], cell["ry"], cell["rz"]), clingo_computed_cells)
    # TODO use cells_dict by default instead of list of cells in block object
    cells_dict = {}

    for cell in block_objective.cells:
        cells_dict[cell.id] = cell

    # here the cells are assigned their tile. Exploits impurity to set the tile in the cell object of the block
    for entry in computed_cells:
        # get all entry parts, meaning the not the last element in the list, that will be the address
        skewed_index = entry[:-4]
        # the skewing is done within the solver
        relative_index = tuple(np.subtract(skewed_index, np.multiply(block_objective_index, block_size)))
        #if not is_in_range(skewed_index, block_objective_index, block_size):
        #    continue
        # relative_index = tuple(np.subtract(skewed_index, only_negative_expanded_boundaries_tuple))
        if not relative_index in cells_dict:
            # print(str(relative_index) +
            #       ": cell ommitted, probably due to boundary expansion")
            continue
        i = i + 1
        cells_dict[relative_index].contains = {(entry[3], *map(int, entry[4:])): block_objective.profile.tiles[entry[3]]}
        # print(f"skewed: {skewed_index}")
        # print(f"relative: {relative_index}")
    print(f"added {i} assignments to cells")
    block_objective.successful = True
    # visualize_voxel(block_objective.show())
    return block_objective

def block_from_result_shape_annotation(solution, block_objective,
                       block_objective_index=(0, 0, 0)):
    block_size = dimensional_dict_to_tuple(block_objective.block_size)
    clingo_computed_cells = solution.values
    computed_cells = [(cell["x"], cell["y"], cell["z"], cell[SHAPE_PLACEMENT_ANNOTATION])
                      for cell in clingo_computed_cells if SHAPE_PLACEMENT_ANNOTATION in cell]
    cells_dict = block_objective.cells_d
    # here the cells are assigned their tile. Exploits impurity to set the tile in the cell object of the block
    for entry in computed_cells:
        # get all entry parts, meaning the not the last element in the list, that will be the address
        skewed_index = entry[:3]
        relative_index = tuple(np.subtract(skewed_index, np.multiply(block_objective_index, block_size)))
        if not relative_index in cells_dict:
            continue

        cells_dict[relative_index].shape_placement_annotation = entry[3]
    return block_objective
