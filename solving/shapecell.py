from solving.cell import Cell


class ShapeCell(Cell):

    def __init__(self, textures, id, cell_size):
        super().__init__(textures, id, cell_size)
        self.shape_data = []