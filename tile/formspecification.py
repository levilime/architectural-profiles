class FormSpecification:

    def __init__(self):
        pass


class BoundingBoxSpecification(FormSpecification):

    def __init__(self, min_size, max_size, horizontal_swappable):
        super().__init__()
        self.min_size = min_size
        self.max_size = max_size
        self.horizontal_swappable = horizontal_swappable
