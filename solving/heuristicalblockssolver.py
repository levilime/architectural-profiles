import json
import random
from functools import reduce

import numpy as np
import copy

from solving.blocksolver import BlockSolver
from solving.metadata import Metadata
from solving.util import merge_dicts, color_connected_parts, dimension_order_with_negative, \
    get_block_solved_surrounding, deep_merge, deep_merge_override_list
from voxels.magicavoxwrapper import visualize_voxel

VISUALIZE_INTERMEDIATE_SUCCESS = False
VISUALIZE_FAILURE = True
ERROR_COLOR = 5

SECOND_LEVEL_SURROUNDING_BLOCKS = 2


def solve_picking_randomely(self, blocks_solve_order: [[]], solver, profile, blocks_dict, block_size, cell_size,
                            empty_block,
                            level, prefer_lower=False, expanded_boundaries=False, always_choose_adjacent=True):
    fail_count = 0
    all_blocks_indexes = get_unique_blocks_from_multiple_block_collection_solve_order \
        (blocks_solve_order)
    blocks_label_indexed = group_multiple_blocks(blocks_solve_order)

    def remaining_blocks():
        return list(filter(lambda index: not blocks_dict[index].void and blocks_dict[index].solution is None,
                    all_blocks_indexes))

    def solved_blocks():
        return set(filter(lambda index: blocks_dict[index].solution,
                    all_blocks_indexes))

    while len(remaining_blocks()) > 0:
        remaining = remaining_blocks()
        solved = solved_blocks()

        print("solved blocks:" + str(len(all_blocks_indexes) - len(remaining)) + " of " + str(len(all_blocks_indexes)))

        if prefer_lower:
            lowest = int(np.min([t[1] for t in remaining]))
            remaining = list(filter(lambda r: r[1] == lowest, remaining))
        if always_choose_adjacent:
            adjacent_solved = [i for i in remaining if [b for b in set(list(blocks_dict[i].neighbors.values()))
                                                        if b.id in solved]]
            remaining = adjacent_solved if adjacent_solved else remaining

        block_index = random.choice(remaining)
        block_indices = [i for i in blocks_label_indexed if blocks_label_indexed[i] ==
                         blocks_label_indexed[block_index]]

        block_surroundings = Metadata.get_surrounding_blocks_static(blocks_dict, SECOND_LEVEL_SURROUNDING_BLOCKS)

        smallest_index = reduce(lambda agg, i: i if np.sum(i) < np.sum(agg) else agg, block_indices)
        relative_block_indices = [tuple(np.asarray(i) - np.asarray(smallest_index)) for i in block_indices]

        # FIXME temporary assertion to debug solving iteratively with a wang tiling roadmap
        # assert(set(relative_metadata_changed[relative_block_indices[0]]["block_equals"]).issuperset(set(relative_block_indices)))

        print("current blocks: " + str(block_indices))
        print("relative indices:" + str(relative_block_indices))
        result = solve_block(solver, profile, blocks_dict, block_indices, block_surroundings, block_size,
                                  cell_size, empty_block, expanded_boundaries)
        if result["success"]:
            self.logger.add_creation_event({}, block_indices, result["result"])
            resolved_blocks = result["solution"]
            for i in resolved_blocks:
                blocks_dict[i].add_solution(resolved_blocks[i])
            # when creating a roadmap for wang tiling, put this solution in all matching tiles in the roadmap
            # same_indices = get_indices_with_same_tile_from_index(block.id, all_block_metadata) \
            #     if "roadmap_tile_color" in all_block_metadata[block.id] else [block.id]
            # for index in same_indices:
            #     blocks_dict[index].add_solution(result["solution"])
            if VISUALIZE_INTERMEDIATE_SUCCESS:
                visualize_voxel(self.show())
        else:
            # restart this block and adjacent blocks
            fail_count += 1
            print(str(block_index) + " failed.")

            class BlockMock:
                def __init__(self, showable):
                    self.showable = showable

                def show(self):
                    return self.showable

                def show_adjacency(self, any):
                    return self.show()

            for i in block_indices:
                blocks_dict[i].add_solution(BlockMock(np.full(self.empty_block.show().shape, ERROR_COLOR)))

            if VISUALIZE_FAILURE:
                visualize_voxel(self.show())
                visualize_voxel(color_connected_parts(self.show_adjacency_type("routing")))

            for i in block_indices:
                blocks_dict[i].remove_solution()
            if fail_count > self.restarts:
                # FIXME this currently leave the blocks that were not restarted
                print(f"assignments failed after {str(fail_count)} tries.")
                break
            deleted_indices = []
            for i in block_indices:
                absolute_surrounding = [tuple(np.add(index, i))
                                        for index in list(get_block_solved_surrounding(i, blocks_dict, level))]
                # restart all surrounding
                deleted_indices += absolute_surrounding
                for surrounding_index in absolute_surrounding:
                    blocks_dict[surrounding_index].solution = None
                    print(str(surrounding_index) + " cascading restart.")
            # delete all blocks that are in the same solve group as a block that is deleted
            deleted_indices_from_group = []
            for i in deleted_indices:
                for group in block_indices:
                    if i in group:
                        deleted_indices_from_group += list(group)
            for i in deleted_indices_from_group:
                blocks_dict[i].solution = None
                print(str(i) + " block equals restart.")



            # remove one or two surrounding the failed block
            # for surrounding_index in [random.choice(absolute_surrounding)]:
            #     blocks_dict[surrounding_index].solution = None
            #     print(str(surrounding_index) + " one block is randomely restarted.")
            print("failed: " + str(fail_count) + " times.")
            print("")


    print("failed: " + str(fail_count) + " times in total.")


def solve_block(solver, profile, blocks_dict, block_indices, surrounding_blocks, block_size, cell_size, empty_block, expanded_boundaries):
    def get_expanded_boundaries(blocks):
        expansion_ordered_to_indices = {}
        for block_index in blocks:
            block = blocks[block_index]
            expanded_boundaries = [d for d in dimension_order_with_negative if d in block.neighbors
                                   and block.neighbors[d].solution is None]
            increased_block_size = reduce(lambda agg, k:
                                          dict(agg, **{k: 1}), expanded_boundaries, {})
            expansion_ordered_to_indices[block_index] = increased_block_size
        return expansion_ordered_to_indices

    expanded_boundaries = get_expanded_boundaries(blocks_dict) if expanded_boundaries else \
        reduce(lambda agg, k: merge_dicts(agg, {k: {}}), blocks_dict, {})


    def create_block_objectives(surrounding_blocks):
        # TODO check if this you should only take block indices or the whole surroundings
        return reduce(lambda agg, i: merge_dicts(agg, {i: BlockSolver(block_size, cell_size, profile,
                      surrounding_blocks.get(i), False, expanded_boundaries[i])}), block_indices,
                      {})


    block_objectives = create_block_objectives(surrounding_blocks)
    def retrieve_solution_with_full_constraint_set_and_also_calculate_borders(blocks):
        def f():
            return solver(block_objectives)
                       #    ,
                       # dict({}, **{"expanded_boundaries": Metadata.get_expanded_boundaries(blocks),
                       #     # "exact_boundary_match": exact_boundary_match,
                       #     "all_block_metadata": relative_all_metadata}))
        return f



    solving_methods = [
        (retrieve_solution_with_full_constraint_set_and_also_calculate_borders(
            reduce(lambda agg, i: merge_dicts(agg, {i: blocks_dict[i]}), block_indices, {})),
         "block: " + str(block_indices) +
         "adjacent neighbor constraint with hard boundary match and expansion"),
    ]
    solution = None
    for solving_method in solving_methods:
        try:
            print("solving technique: " + solving_method[1])
            solution = solving_method[0]()
            # visualize_voxel(solution.show())
        #     break
        except ValueError as err:
            print(str(block_indices) + ": fails " + solving_method[1])
            print(err)
            return {"success": False}

    return {"success": not not solution, "solution": block_objectives, "result": solution}


def get_unique_blocks_from_multiple_block_collection_solve_order(multiple_block_collection_solve_order):
    return reduce(lambda agg, indices: agg.union(indices),
                                multiple_block_collection_solve_order, set())


def get_unique_blocks_from_multiple_block_collection_solve_order_labeled(multiple_block_collection_solve_order):
    return reduce(lambda agg, t: agg.union([(t[0], index) for index in t[1]]),
                                enumerate(multiple_block_collection_solve_order), set())


def group_multiple_blocks(multiple_block_collection_solve_order):
    labeled_indices = get_unique_blocks_from_multiple_block_collection_solve_order_labeled(
        multiple_block_collection_solve_order)
    return reduce(lambda agg, t: merge_dicts(agg, {t[1]: t[0]}), labeled_indices, {})