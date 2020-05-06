from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class BuildingWithinBlock(DeclarativeConstraints):

    def __init__(self):
        building_stay_within_block = DeclarativeConstraint(
        "Buildings stay within a block",
        ":- assign(X,Y,Z,ID), category(ID, building), X = xsize, not match(x, empty_space_outside, ID).\n"
        ":- assign(X,Y,Z,ID), category(ID, building), X = 0, not match(minusx, empty_space_outside, ID).\n"
        ":- assign(X,Y,Z,ID), category(ID, building), Y = ysize, not match(y, empty_space_outside, ID).\n"
        ":- assign(X,Y,Z,ID), category(ID, building), Y = 0, not match(minusy, empty_space_outside, ID).\n"
        ":- assign(X,Y,Z,ID), category(ID, building), Z = zsize, not match(z, empty_space_outside, ID).\n"
        ":- assign(X,Y,Z,ID), category(ID, building), Z = 0, not match(minusz, empty_space_outside, ID).\n"
        )
        super().__init__([
            building_stay_within_block
                          ])
