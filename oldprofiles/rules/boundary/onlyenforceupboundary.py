from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class OnlyEnforceUpBoundaryMatch(DeclarativeConstraints):

    def __init__(self):
        # this rule checks:
        # given the edge directions where there is no neighbor block,
        # let there not be a tile that is not overidden to reside at the edge of an empty edge.
        leave_up_boundary = DeclarativeConstraint(
            "leave up boundary for empty boundary match.",
            "adjacentblockneighbor(x).adjacentblockneighbor(minusx).adjacentblockneighbor(z)"
            ".adjacentblockneighbor(minusz).adjacentblockneighbor(minusy)."
        )
        super().__init__([leave_up_boundary])