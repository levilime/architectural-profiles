from functools import reduce

from solving.logging.event import Event
from solving.util import merge_dicts


class DestructionEvent(Event):

    def __init__(self, time, block_dimensions, failed_block, destroyed_blocks, profile):
        super().__init__(time, failed_block, block_dimensions, False)
        self.destroyed_blocks = destroyed_blocks
        self.profile = profile

    def output(self):
        d = {
            "type": "failure",
            "destroyed_blocks": [block.id for block in self.destroyed_blocks],
            "profile": self.profile.get_profile_json()
        }
        return merge_dicts(super().output(), d)


