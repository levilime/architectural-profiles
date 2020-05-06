from solving.logging.creationevent import CreationEvent
from solving.logging.destructionevent import DestructionEvent


class SolvingLogger:

    def __init__(self):
        self.events = []

    # def add_destruction_event(self, time, block_dimensions, failed_block, destroyed_blocks, profile):
    #     self.events.append(DestructionEvent(time, block_dimensions, failed_block, destroyed_blocks, profile))
    #
    def add_creation_event(self, block_dimensions, blocks, solution, profile={}):
        self.events.append(CreationEvent(0, blocks, block_dimensions, solution, profile))

    #
    # def count_failures(self):
    #     return len([x for x in self.events if not x.success])
    #
    def output_events(self):
        return [e.output() for e in self.events]
