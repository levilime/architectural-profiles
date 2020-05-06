import json
from functools import reduce

from solving.util import merge_dicts


class ShapeMetadata:

    def __init__(self, pulled_by_gravity=False, entrance_amount=False, entrance_vertical_levels=False,
                 shape_occurence=False):
        """
        :param pulled_by_gravity:
        :param entrance_amount: list is expected, interpreted as a range of numbers
        :param entrance_vertical_levels: list is expected, interpreted as a set of numbers
        :param shape_occurence: JSON {grid: [], amount: Number}
        """
        self.pulled_by_gravity = pulled_by_gravity
        self.entrance_amount = entrance_amount
        self.entrance_vertical_levels = entrance_vertical_levels
        self.occurence = ShapeOccurence(shape_occurence) if shape_occurence else False

class ShapeOccurence:

    def __init__(self, json_obj):
        if not "grid" in json_obj:
            raise ValueError("shape occurence does not have an occurence grid entry")
        self.grid = json_obj.get("grid") # [x,y,z]
        self.amount = json_obj.get("amount") # [min, max]


class AbstractShapeSpecification:

    def __init__(self, name, form):
        self.name = name
        self.form = form

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name



class ShapeSpecification(AbstractShapeSpecification):

    def __init__(self, name, t, category, form, shape_metadata=ShapeMetadata()):
        '''
        :param name:
        :param t:
        :param category:
        :param form: form of the shape, currently a dict
        {type: string, min: tuple(int), max: tuple(int), horizontalswap: bool}
        '''
        self.type = t
        self.category = category
        self.shape_metadata = shape_metadata
        super().__init__(name, form)


class NonAtomicShapeSpecification(AbstractShapeSpecification):

    def __init__(self, name, form, shapes, closed_types):
        self.shapes = shapes
        self.closed_types = closed_types
        super().__init__(name, form)


def create_specifications_from_json(profile_json):
    atomic_shapes = reduce(lambda agg, e: merge_dicts(agg, {e["id"]:
                                ShapeSpecification(e["id"], e["type"], e["category"], e["form"],
                                                   ShapeMetadata(
                                                       pulled_by_gravity=e.get("pulledbygravity", False),
                                                       entrance_amount=e.get("entrances", []),
                                                       entrance_vertical_levels=e.get("entranceatlevel", []),
                                                       shape_occurence=e.get("occurence", False)))
                                                            }),
                           (e for e in profile_json.get("shapes", []) if not e.get("nonatomic", False)), {})
    non_atomic_shapes = reduce(lambda agg, e: merge_dicts(agg, {e["id"]:
                            NonAtomicShapeSpecification(e["id"], e["form"], e["shapes"], e["closeontypes"])}),
                           (e for e in profile_json.get("shapes", []) if e.get("nonatomic", False)), {})
    return merge_dicts(atomic_shapes, non_atomic_shapes)


class Tree:

    def __init__(self, name):
        self.name = name
        self.children = set()

    def __hash__(self):
        return hash(self.name)

    def add_child(self, node):
        self.children.add(node)

    def iterate_over_tree(self):
        acc = []
        for child in self.children:
            acc.extend(child.iterate_over_tree())
        acc.append(self)
        return acc


def order_shapes(shapes):
    """
    Order shapes according to their solve order given the dependencies of non atomic shapes
    :param shapes:
    :return: ordered shapes
    """
    nodes = {}
    for shape_specification in shapes:
        node = Tree(shape_specification.name)
        nodes[shape_specification.name] = node

    for shape_specification in shapes:
        if type(shape_specification) != ShapeSpecification:
            for shape_id in shape_specification.shapes:
                nodes[shape_specification.name].add_child(nodes[shape_id])

    roots = set(nodes.values()).difference(reduce(lambda agg, node: agg.union(node.children), nodes.values(), set()))
    print()
    ordered = reduce(lambda agg, root: agg + root.iterate_over_tree(), roots, [])
    return sorted(shapes, key=lambda shape_specification: ordered.index(nodes[shape_specification.name]))



