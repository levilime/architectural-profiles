from functools import reduce

from solving.util import deep_merge, invert_dimension, merge_dicts

class CutOffs:

    def __init__(self, serialized_cutoffs):
        self.cutoffs = []
        for cutoff in serialized_cutoffs:
            self.cutoffs.append(CutOff(cutoff["types"], cutoff["categories"]))


class CutOff:

    def __init__(self, types, categories):
        self.types = types
        self.categories = categories

    def serialize(self):
        return {"types": self.types, "categories": self.categories}