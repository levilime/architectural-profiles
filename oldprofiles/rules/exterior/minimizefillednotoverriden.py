from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class MinimizeFilledNotTilesOverriden(DeclarativeConstraints):

    def __init__(self):
        minimize_filled_tiles_not_override = DeclarativeConstraint(
            "Minimize not overriden filled tiles.",
            "filledcategoryinnotoverrideamount(A) :- A = #count{X,Y,Z: assign(X,Y,Z,I), not overridefilled(X,Y,Z), texture(I, _, _, _, _, _, _),\n" \
                   "category(I, filled)}.\n"
            "#minimize { Y@1: filledcategoryinnotoverrideamount(Y) }."
        )
        super().__init__([minimize_filled_tiles_not_override])
