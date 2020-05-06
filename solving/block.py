class Block:
    """
    Block consists of references to neighbor blocks and a solution.
    Used as an element in simplesolver
    """
    def __init__(self, id, void=False):
        self.id = id
        self.neighbors = {}
        self.solution = None
        self.void = void

    def add_neighbors(self, neighbors):
        self.neighbors = neighbors

    def add_solution(self, solution):
        self.solution = solution

    def remove_solution(self):
        self.solution = None

    # def copy(self):
    #     return self._copy({})
    #
    # def _copy(self, trace):
    #     new_block = Block(self.id)
    #     new_block.add_solution(self.solution)
    #     trace[self.id] = True
    #     new_block.add_neighbors(
    #         list(map(lambda neighbor: neighbor._copy(trace),
    #                  [neighbor for neighbor in self.neighbors if neighbor not in trace])))
    #     return new_block




