from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class EmptyBoundaryMatchIgnoreDoor(DeclarativeConstraints):

    def __init__(self):
        ignore_route = DeclarativeConstraint(
            "Routes can go to an empty boundary, needs emptyboundarymatch to work",
            "overrideempty(door)."
        )
        super().__init__([ignore_route])