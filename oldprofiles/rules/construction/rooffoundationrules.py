from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class RoofFoundationRules(DeclarativeConstraints):

    def __init__(self):
        roof_not_directly_above_foundation = DeclarativeConstraint(
            "a roof can never be directly above a foundation, because there would be empty space in between.",
            ":- assign(X1, Y1, Z1, ID1), category(ID1, roof), 1 {assign(X1, Y1 - 1, Z1, ID2): category(ID2, foundation)}."
        )
        no_roof_floating_in_the_air = DeclarativeConstraint(
            "a roof can never be directly above a foundation, because there would be empty space in between.",
            ":- assign(X1, Y1, Z1, ID1), category(ID1, roof), 1 {assign(X1, Y1 - 1, Z1, ID2): category(ID2, void)}."
        )
        foundation_not_directly_above_roof = DeclarativeConstraint(
            "a foundation can never be directly below a roof, because there would be no space in between.",
            ":- assign(X1, Y1, Z1, ID1), category(ID1, foundation), 1 {assign(X1, Y1 + 1, Z1, ID2): category(ID2, roof)}."
        )
        roof_can_only_be_directly_above_building = DeclarativeConstraint(
            "roof can only be directly above building",
            ":- assign(X1, Y1, Z1, ID1), category(ID1, roof), assign(X1, Y1 - 1, Z1, ID2), not category(ID2, building)."
        )
        super().__init__([roof_not_directly_above_foundation,
                          foundation_not_directly_above_roof,
                          no_roof_floating_in_the_air,
                          roof_can_only_be_directly_above_building])
