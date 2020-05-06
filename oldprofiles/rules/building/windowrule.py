from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoEmptyTilesRule(DeclarativeConstraints):

    def __init__(self):
        window_facade_distance = DeclarativeConstraint(
            "% direction 0, perpendicular to z, pointing to z+ then clockwise (1: x+, 2: -z, 3:-x).\n" +
            "% if there is a window then at the direction orthogonal to the window outside, at least one empty space must be created",
            ":- assign(X1,Y1,Z1,ID1), category(ID1, boundary), category(ID1, window), direction(ID1, D), hasadjacacencytodirection(X1,Y1,Z1,D),\n" +
            "directiontoadjacency(X1,Y1,Z1,D,X2,Y2,Z2),\n" +
            "not 1 {assign(X2,Y2,Z2,ID2): category(ID2, void)}."
        )
        super().__init__([window_facade_distance])
