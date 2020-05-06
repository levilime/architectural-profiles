from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class OnlyOneBuildingLevel(DeclarativeConstraints):

    def __init__(self):
        one_inside = DeclarativeConstraint(
        "There can never be two floors above each other.",
        ":- assign(X1,Y1,Z1,ID1), assign(X2,Y2,Z2,ID2), adjacent(X1,Y1,Z1,X2,Y2,Z2), Y1 != Y2, " +
        "1 {category(ID1, interior): category(ID2, interior)}."
        )
        super().__init__([one_inside])
