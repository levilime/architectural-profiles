from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoCornerAdjacency(DeclarativeConstraints):

    def __init__(self):
        corner_never_adjacent_to_other_corner = DeclarativeConstraint(
            "no corner boundaries adjacent to each other",
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), Y1 = Y2, category(ID1, corner),\n"
            "category(ID2, corner), assign(X2, Y2, Z2, ID2).\n"
            "%1 {cell(X1, Y1, Z1): category(ID2, wall), category(ID2, straight)} :- assign(X1, Y1, Z1, ID1), assign(X2, Y2, Z2, ID2), \n"
            "%Y1 = Y2, adjacent(X1, Y1, Z1, X2, Y2, Z2), category(ID1, corner)."
        )
        corner_always_adjacent_to_wall = DeclarativeConstraint(
            "corner has at least a wall at one side. Needs routedirections for corners",
            # "%assign(X1,Y1,Z1, ID1) :- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X2,Y2,Z2, ID2), \n"
            # "%category(ID1, corner), category(ID2, wall).\n"
            # "1 {assign(X2, Y2, Z2, ID2): category(ID2, wall), adjacent(X1, Y1, Z1, X2, Y2, Z2), \n"
            # "match(XDiff, YDiff, ZDiff, ID1, ID2), X1 = X2 + XDiff, Y1 = Y2 + YDiff, Z1 = Z2 + ZDiff } :- \n"
            # "assign(X1, Y1, Z1, ID1), category(ID1, corner)."
            ":- assign(X1, Y1, Z1, ID1), category(ID1, corner), \n"
            "not 1 {assign(X2, Y2, Z2, ID2): routedirection(ID1, Direction), \n"
            "directionmap(Direction, X1, Y1, Z1, X2, Y2, Z2), assign(X2, Y2, Z2, ID2), \n"
            "category(ID2, wall)}."
        )

        super().__init__([
            # corner_never_adjacent_to_other_corner,
            corner_always_adjacent_to_wall
        ])

# this stuff was used to debug corner:
# "\nassign(1,1,1,inside)."
# "\nassign(2,1,2,corner_boundary0).""\nassign(0,1,0,corner_boundary2)."