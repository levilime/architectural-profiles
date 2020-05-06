from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class EmptyBoundaryMatch(DeclarativeConstraints):

    def __init__(self):
        # this rule checks:
        # given the edge directions where there is no neighbor block,
        # let there not be a tile that is not overridden to reside at the edge of an empty edge.
        empty_boundary_match = DeclarativeConstraint(
            "If the solution end at a certain side, the tiles on that edge must match with the empty tile",
            ":- direction(Direction), not adjacentblockneighbor(Direction), \n"
            "1 {assign(X,Y,Z,ID): edgepositions(Direction, X,Y,Z), "
            "not match(Direction, empty_space_outside, ID), category(ID, Category), not overrideempty(Category)}."
            #", Y > 0; not blockfilledunder}."
        )
        ignore_filled_by_default = DeclarativeConstraint(
         "ignore filled by default",
         "overrideempty(filled)."
        )
        super().__init__([empty_boundary_match, ignore_filled_by_default])