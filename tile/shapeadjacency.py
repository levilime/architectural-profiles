class ShapeAdjacency:

    def __init__(self, shape_a, shape_b):
        self.shape_a = shape_a
        self.shape_b = shape_b
        # if directed is True, then adjacency only goes from a -> b
        self.directed = False

    def has_type(self, t):
        return self.shape_a.has_type(t) and self.shape_b.has_type(t)

    def has_category(self, c):
        return self.shape_a.has_category(c) or self.shape_b.has_category(c)

    def has_category_pair(self, c_a, c_b):
        return (self.shape_a.has_category(c_a) and self.shape_b.has_category(c_b)) or \
               (self.shape_b.has_category(c_a) and self.shape_a.has_category(c_b))


class HierarchicShapeAdjacency(ShapeAdjacency):

    def __init__(self, shape_a, shape_b):
        super().__init__(shape_a, shape_b)
        self.directed = True


class ShapeAdjacencies:

    def __init__(self, adjacencies):
        self.adjacencies = adjacencies

    def __len__(self):
        len(self.adjacencies)

    def get_shapes_that_have_adjacency_with_shape(self, shape):
        return [
            a.shape_b if shape.equals(a.shape_a) else a.shape_a for a in self.adjacencies
            if shape.equals(a.shape_a) or shape.equals(a.shape_b)
        ]

    def add_adjacency(self, adjacency):
        return ShapeAdjacencies(self.adjacencies + adjacency)

    def get_adjacencies_by_category_pair(self, category_a, category_b):
        return ShapeAdjacencies(filter(lambda adjacency:
                                       adjacency.has_category_pair(category_a, category_b),
                                       self.adjacencies))

    def get_adjacencies_by_category(self, category):
        return ShapeAdjacencies(filter(lambda adjacency: adjacency.has_category(category),
                                       self.adjacencies))

    def get_adjacencies_by_categories(self, categories):
        return ShapeAdjacencies(filter(lambda adjacency:
                                       [category for category in categories if adjacency.has_category(category)],
                                       self.adjacencies))

    def get_adjacencies_by_type(self, t):
        return ShapeAdjacencies(filter(lambda adjacency: adjacency.has_type(t), self.adjacencies))
