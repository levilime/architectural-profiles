from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class OnlySmallBuilding(DeclarativeConstraints):

    def __init__(self):
        only_small_building = DeclarativeConstraint(
            "Only Small buildings are allowed as buildings.",
            ":- assign(X,Y,Z,ID), category(ID, interior), not category(ID, small_building)."
        )
        super().__init__([only_small_building])

