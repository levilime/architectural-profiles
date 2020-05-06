from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class BuildingDensityRules(DeclarativeConstraints):

    def __init__(self, ratio=1):
        keep_empty_and_built_ratio_equal = DeclarativeConstraint(
            "Keep empty and built ratio equal.",
            "#minimize { |Y * 1 - Z * " + str(ratio) +"|@1, X: assign(_,_,_,X),  textureswithtag(void, Y), textureswithtag(inside, Z)}."
        )
        super().__init__([keep_empty_and_built_ratio_equal])
