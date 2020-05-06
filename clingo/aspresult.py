import re
from functools import reduce
import numpy as np

from solving.util import dimension_order, dimensional_tuple_to_dict, merge_dicts, list_to_d

SOLUTION_ID_TOKEN = "solution_id"
SHAPE_PLACEMENT_ANNOTATION = "shape_placement"

class Result:

    def __init__(self, json_obj):
        self.information = json_obj
        self.solutions = []
        if json_obj.get("Result", "SATISFIABLE") == "SATISFIABLE" or \
                json_obj.get("Result", "") == "OPTIMUM FOUND":
            self.solutions = [ShapeSolution(obj) for obj in json_obj["Call"][0]["Witnesses"]]
        self.time = json_obj.get("Time", {})

    def to_json(self):
        return {"raw": self.information, "solutions": [x.to_json() for x in self.solutions]}

    @staticmethod
    def create_from_json(json_obj):
        return Result(json_obj["raw"])

    def merge(self, result):
        self.solutions += result.solutions
        self.time = reduce(lambda agg, k: merge_dicts(agg,
                                                      dict(k=self.time.get(k, 0) + result.time.get(k,0))),
                           self.time,
                           {})


class Solution:
    def __init__(self, solution_obj):
        self.values = consume_clingo_output(solution_obj["Value"])
        self.score = solution_obj.get("Costs", 99999)
        self.optimization_values = {"uniquetiles": None, "densityscore": None}
        self.consume_optimization_values(solution_obj["Value"])

    def to_json(self):
        return {"optimization": self.optimization_values, "values": self.values}

    def represented_block_size(self):
        min_value, max_value = reduce(lambda t, value: (
            np.minimum(value, t[0]),
            np.maximum(value, t[1])
        ) if t else (np.asarray(value), np.asarray(value)),
                                      [tuple([v[d] for d in dimension_order]) for v in self.values], None)

        box_size = (max_value - min_value + 1).tolist()
        return dimensional_tuple_to_dict(box_size), min_value

    def consume_optimization_values(self, solution):
        # consume assigns
        for cell in solution:
            elem = re.search(r'assign\(.*\)', cell)
            if elem is None:
                elem = re.search(r'(\w|\d)*\(.*\)', cell)
                elem = elem.group()
                subject = elem.split("(")[0]
                value = elem.split("(")[1].split(")")[0]
                if subject in self.optimization_values:
                    self.optimization_values[subject] = int(value)


def assign_search(cell):
    return re.search(r'assign\(.*\)', cell)


def consume_clingo_output(solution):
    cells = []
    # consume assigns
    for cell in solution:
        elem = assign_search(cell)
        if elem is None:
            # print(f"not assign: {cell}.")
            continue
        elem = elem.group().replace("assign(", "").replace(")", "")
        elem = elem.split(",")
        cells.append({"rx": elem[4], "ry": elem[5], "rz": elem[6], "x": int(elem[0]), "y": int(elem[1]),
                      "z": int(elem[2]), SOLUTION_ID_TOKEN: elem[3]})
    return cells


def consume_clingo_shape_output(solution):
    cells = []
    # consume assigns
    for cell in solution:
        elem = re.search(r'shapeplacement\(.*\)\)', cell)
        if elem is None:
            # print(f"not assign: {cell}.")
            continue
        elem = elem.group().replace("shapeplacement(", "").replace("(", "").replace(")", "")
        elem = elem.split(",")
        cells.append({"x": int(elem[4]), "y": int(elem[5]), "z": int(elem[6]), SHAPE_PLACEMENT_ANNOTATION: cell+"."})
    return cells


def attach_clingo_shape_output_to_cell_output(solution, cells):
    """

    :param solution:
    :param cells: assumes the cells are in the same order as the solution
    :return:
    """
    solution_d = list_to_d(cells, "x", "y", "z")
    shape_placement_d = list_to_d(consume_clingo_shape_output(solution), "x", "y", "z")
    all_outside = []
    if not set(solution_d).issuperset(shape_placement_d):
        all_outside = [shape_placement_d[k] for k in set(solution_d).difference(shape_placement_d)]
    return [merge_dicts(solution_d[k], shape_placement_d[k])
            if k in shape_placement_d else solution_d[k] for k in solution_d] + all_outside


class ShapeSolution(Solution):

    def __init__(self, solution_obj):
        super().__init__(solution_obj)
        self.values = attach_clingo_shape_output_to_cell_output(
            solution_obj["Value"], self.values)
