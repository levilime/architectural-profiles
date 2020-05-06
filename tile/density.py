import json

class Density:

    def __init__(self, serialized_density):
        self.density = serialized_density

    def serialize(self):
        return {"density": self.density}