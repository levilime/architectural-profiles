from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class ThereMustBeInside(DeclarativeConstraints):

    def __init__(self):
        there_must_be_a_door = DeclarativeConstraint(
            "For testing, there must be an door.",
            "1 {assign(X,Y,Z, ID):cell(X, Y, Z), category(ID, door)}."
        )
        super().__init__([
                          there_must_be_a_door,
                          ])
