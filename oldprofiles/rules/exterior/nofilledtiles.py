from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoFilledTiles(DeclarativeConstraints):

    def __init__(self):
        no_filled_tiles = DeclarativeConstraint(
            "No filled tiles, these were only created for creating overriding edges.",
            ":- category(ID, filled), assign(X, Y, Z, ID), not override(X,Y,Z).\n"
            "#maximize { Y@2: filledcategoryinoverrideamount(Y) }."
        )
        super().__init__([no_filled_tiles])
