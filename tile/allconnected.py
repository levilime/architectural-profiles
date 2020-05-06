from functools import reduce

from solving.util import deep_merge, invert_dimension


class AllConnected:

    def __init__(self, serialized_all_connected):
        self.all_connected = [AllConnectedPart(dic["type"], dic["category"], dic["level"] if "level" in dic else 1) for dic in serialized_all_connected]

    def serialize(self):
        return {"allconnected": [c.serialize() for c in self.all_connected]}


class AllConnectedPart:

    def __init__(self, type_c, category, level=1):
        self.type = type_c
        self.category = category
        self.level = level

    def serialize(self):
        return {"type": self.type, "category": self.category, "level":self.level}
