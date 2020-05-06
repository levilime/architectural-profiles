from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class MaximizeVariety(DeclarativeConstraints):

    def __init__(self):
        maximize_variety = DeclarativeConstraint(
            "% optimization to create as much variety as possible, by maximimazing the amount of texturegroups present.",
            "#maximize { Y@1, X: texturegroup(Id, X), assign(_,_,_,Id), uniquegroups(Y) }."
        )
        super().__init__([maximize_variety])

