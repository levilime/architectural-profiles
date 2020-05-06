from solving.logging.event import Event
from solving.util import merge_dicts


class CreationEvent(Event):

    def __init__(self, time, block_dimensions, block, solution, profile):
        super().__init__(time, block, block_dimensions, True)
        self.solution = solution
        self.profile = profile

    def output(self):
        d = {
            "type": "success",
            "solution": self.solution.to_json() #,
            #"profile": self.profile.get_profile_json()
        }
        return d
        # merge_dicts(super().output(), d)
