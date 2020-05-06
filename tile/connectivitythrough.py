class ConnectivityThrough:

    def __init__(self, d):
        self.type = d["type"]
        self.category_a = d["category_a"]
        self.category_b = d["category_b"]
        self.category_c = d["category_c"]


class ConnectivityThroughs:

    def __init__(self, serialized_throughs):
        self.throughs = [ConnectivityThrough(d) for d in serialized_throughs]

