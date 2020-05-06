from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class RoofOnlyDirectlyAboveBuilding(DeclarativeConstraints):

    def __init__(self):
        roof_can_only_be_directly_above_building = DeclarativeConstraint(
            "roof can only be directly above building",
            ":- assign(X1, Y1, Z1, ID1), category(ID1, roof), assign(X1, Y1 - 1, Z1, ID2), not category(ID2, building)."
        )

        super().__init__([roof_can_only_be_directly_above_building
                          ])
