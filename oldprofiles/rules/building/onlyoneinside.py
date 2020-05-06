from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class OnlyOneTileInside(DeclarativeConstraints):

    def __init__(self):
        one_inside = DeclarativeConstraint(
        "There can only be one inside next to each other, will result in small homogenous houses.",
        ":- assign(X1,Y1,Z1,ID1), assign(X2,Y2,Z2,ID2), adjacent(X1,Y1,Z1,X2,Y2,Z2), " +
        "1 {texturegroup(ID1, inside): texturegroup(ID2, inside)}."
        )
        super().__init__([one_inside])
