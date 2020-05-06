from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoStairs(DeclarativeConstraints):

    def __init__(self):
        # this rule checks:
        # given the edge directions where there is no neighbor block,
        # let there not be a tile that is not overidden to reside at the edge of an empty edge.
        no_stairs = DeclarativeConstraint(
            "No stairs can be assigned.",
            ":- assign(_, _, _, ID), category(ID, vertical), category(ID, routing)."
        )
        super().__init__([no_stairs])