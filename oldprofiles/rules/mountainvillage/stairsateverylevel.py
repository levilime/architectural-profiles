from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class StairsAtEveryLevel(DeclarativeConstraints):

    def __init__(self):
        stairs_every_level = DeclarativeConstraint(
            "Stairs at every level.",
            "level(Y) :- cell(X,Y,Z).\n"
            "1 {assign(X,Y,Z, ID):cell(X, Y, Z), texturegroup(ID, stairs)} :- level(Y), not Y = ysize."
        )
        super().__init__([stairs_every_level])

