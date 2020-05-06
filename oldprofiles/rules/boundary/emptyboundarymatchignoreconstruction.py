from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class EmptyBoundaryMatchIgnoreContruction(DeclarativeConstraints):

    def __init__(self):
        ignore_route = DeclarativeConstraint(
            "Construction can go to an empty boundary, needs emptyboundarymatch to work.",
            "overrideempty(construction)."
        )
        super().__init__([ignore_route])
