from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoRoof(DeclarativeConstraints):

    def __init__(self):
        no_roof = DeclarativeConstraint(
            "No roof.",
            ":- assign(X,Y,Z,ID), cell(X,Y,Z), texturegroup(ID, roof)."
        )
        super().__init__([no_roof])

