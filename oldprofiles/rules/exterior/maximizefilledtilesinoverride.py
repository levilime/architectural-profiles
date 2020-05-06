from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class MaximizeFilledTilesinOverride(DeclarativeConstraints):

    def __init__(self):
        maximize_filled_tiles_override = DeclarativeConstraint(
            "Maximize overriden filled tiles.",
            "filledcategoryinoverrideamount(A) :- A = #count{X,Y,Z: assign(X,Y,Z,I), overridefilled(X,Y,Z), texture(I, _, _, _, _, _, _),\n" \
                   "category(I, filled)}.\n"
            "#maximize { Y@3: filledcategoryinoverrideamount(Y) }."
        )
        super().__init__([maximize_filled_tiles_override])
