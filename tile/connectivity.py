from functools import reduce

from solving.util import deep_merge, invert_dimension, merge_dicts


class Connectivities:

    def __init__(self, serialized_connectivity):
        self.connectivities = []
        for type in serialized_connectivity:
            for routes in serialized_connectivity[type]["categories"]:
                self.connectivities.append(
                    Connectivity(type, routes["start"], routes["through"], routes["end"],
                                 tuple([routes["length"]["minimum"], routes["length"]["maximum"]]))
                )


    def get_all_routing_routes(self):
        return list(filter(lambda c: c.type == "routing", self.connectivities))

    def get_all_routes(self):
        return self.connectivities

    def serialize(self):
        elements = [{e.type: {"categories": [e.serialize()]}} for e in self.connectivities]
        return {"connectivity": reduce(deep_merge, elements, {})}


class Connectivity:

    def __init__(self, type, from_c, through_c, to_c, length):
        self.type = type
        self.from_c = from_c
        self.through_c = through_c
        self.to_c = to_c
        self.length = length

    def serialize(self):
        return {"type": self.type, "start": self.from_c, "through": self.through_c, "end": self.to_c,
                "length": {"minimum": self.length[0], "maximum": self.length[1]}}
