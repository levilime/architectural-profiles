from functools import reduce
import random

from solving.util import invert_dimension

switcheroo = {
    "x": "-x",
    "-x": "x",
    "y": "y",
    "-y": "-y",
    "-z": "z",
    "z": "-z"
}

def solve_simple(self):
    """
    Heuristicentry = a[0] ally (greedily) finds a satisfying tile composition contained within the cells.
    :return: the BlockSolver object
    """
    while not done(self.cells):
        # choose the cell next that has the least amount of possibilities left. (Most obvious to choose from)
        transitional_cells = sorted(transitional_cells_f(self.cells), key=lambda x: len(x.contains))
        chosen_cell = transitional_cells[0]
        remaining_choices = choose_conforming_to_neighbors(chosen_cell)
        if not remaining_choices:
            print("error")
            self.successful = False
            chosen_cell.contains = remaining_choices
            continue
        choose_key = list(remaining_choices)[random.randint(0, len(remaining_choices) - 1)]
        chosen_transition = {choose_key: chosen_cell.contains[choose_key]}
        make_choice_propagate(chosen_cell, chosen_transition)
    self.successful = True if self.successful is None else False
    return self

def transitional_cells_f(cells):
    return [cell for cell in cells if len(cell.contains) > 1]

def done(cells):
    return reduce(lambda agg, cell: len(cell.contains) < 2 and agg, cells, True)


def choose_conforming_to_neighbors(cell):
    """
    Compare neighbors to see if there are any textures(states) that are not valid anymore within the cell
    :param cell:
    :return: the remaining states
    """
    remaining_states = cell.contains
    # make a reverse map for the filter states function
    for neighbor_key in cell.neighbors:
        remaining_states = filter_states(remaining_states, cell.neighbors[neighbor_key].contains,
                                         switcheroo[neighbor_key])
    return remaining_states


def propagate_over_neighbors(chosen_cell, trace):
    """
    Administer the decision for the remaining states in the chosen cell to the surounding cells. Meaning
    the surrounding cells may lose states.
    :param chosen_cell:
    :param trace:
    :return: void, this function mutates the object
    """
    for neighbor_key in chosen_cell.neighbors:
        # if not chosen_cell.neighbors[neighbor_key].id in trace:
        #     trace[chosen_cell.neighbors[neighbor_key].id] = 0
        # elif trace[chosen_cell.neighbors[neighbor_key].id] < 2:
        #     trace[chosen_cell.neighbors[neighbor_key].id] += 1
        # else:
        #     return
        propagate(chosen_cell.neighbors[neighbor_key], chosen_cell, neighbor_key, trace)


# currently greedily make one choice and commit to it, no way to undo choices
def make_choice_propagate(chosen_cell, chosen_transition):
    chosen_cell.contains = chosen_transition
    propagate_over_neighbors(chosen_cell, {chosen_cell.id: 2})


def propagate(chosen_cell, previous_cell, relation, trace):
    """
    filter chosen cell states according to previous_cell states through the relation
    :param chosen_cell:
    :param previous_cell:
    :param relation:
    :param trace:
    :return:
    """
    chosen_cell.contains = filter_states(chosen_cell.contains, previous_cell.contains, relation) if len(
        chosen_cell.contains) > 1 else chosen_cell.contains
    # commenting the line underneath makes it update constraints only for direct neighbors
    # this makes it look only locally but kills the recursion and therefore only needs a limited amount
    # of memory
    # propagate_over_neighbors(chosen_cell, trace)

# TODO move this in a utility file, it is more general than just for one solver
# relationship is from the cell with possible to the cell with containing. So if containing is right
# from possible than the relation is "x"
def filter_states(containing, possible, relation):
    """
    Filter the states(textures) within a cell that are not satisfied anymore
    :param containing: the textures that are in the cell
    :param possible: the cells that are adjacent through the relation with the cell
    :param relation: a direction for which the containing and possible need to be compared and filtered.
    direction of the relation is from possible towards containings
    :return: the states from containing that fit the constraints imposed by possible
    """
    remaining_states = {}
    for poss_state in possible:
        for con_state in containing:
            if con_state in possible[poss_state].constraints[relation]:
                remaining_states[con_state] = containing[con_state]
    return remaining_states
