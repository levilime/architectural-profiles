from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoEmptyTilesRule(DeclarativeConstraints):

    def __init__(self):
        no_filled_tiles = DeclarativeConstraint(
            "No empty tiles can be assigned.",
            ":- assign(_, _, _, ID), category(ID, void)."
        )
        super().__init__([no_filled_tiles])
