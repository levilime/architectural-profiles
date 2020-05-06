

from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class PlaceNoFilled(DeclarativeConstraints):

    def __init__(self):
        there_must_be_place_where_no_filled = DeclarativeConstraint(
            "There must be a place where there is no filled.",
            "1 {assign(X,0,Z, ID):cell(X, 0, Z), texturegroup(ID, floorroof)}."
        )

        super().__init__([there_must_be_place_where_no_filled
                          ])

