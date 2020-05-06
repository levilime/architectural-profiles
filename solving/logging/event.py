class Event:

    def __init__(self, time, block, block_dimensions, success):
        self.time = time
        self.block = block
        self.block_dimensions = block_dimensions
        self.success = success

    def output(self):
        return {"block_id": self.block.id,
                "block_dimensions": self.block_dimensions,
                "time": self.time}
