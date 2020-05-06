from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class BuildingsNotBuiltOnAir(DeclarativeConstraints):

    def __init__(self):

        buildings_may_not_be_built_on_air = DeclarativeConstraint(
            "Buildings may not be built on air.",
            ":- assign(X1,Y1,Z1, ID1), category(ID1, building), assign(X1, Y1 - 1, Z1, ID2), \n"
            "category(ID2, void)."
        )

        super().__init__([buildings_may_not_be_built_on_air
                          ])

