from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class HardConstraintFilledTilesinOverride(DeclarativeConstraints):

    def __init__(self):
        hard_constraint_filled_tiles_override = DeclarativeConstraint(
            "Hard constraint filled tiles.",
            "1 {assign(X, Y, Z" + ", ID): texture(ID,_, _, _, _, _, _), category(ID, filled)} 1 :- override(X,Y,Z),\n"
            "overridefilled(X,Y,Z), currentblock(X,Y,Z).\n"
            "assign(X,Y,Z, ID):- texture(ID, _,_,_,_,_,_), category(ID, filled),  overridefilled(X,Y,Z), "
            "not currentblock(X,Y,Z).\n"
        )
        super().__init__([hard_constraint_filled_tiles_override])
