from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class BlockFloorIsFilled(DeclarativeConstraints):

    def __init__(self):
        add_exception = DeclarativeConstraint(
            "add exception used by other rules to account for block floor is filled",
            "blockfilledunder :- not adjacentblockneigbor(minusy)."
        )

        block_floor_is_filled = DeclarativeConstraint(
            "Take into account that tiles on the lowest layer on the minusy edge must match with filled",
            ":- blockfilledunder, \n"
            "1 {assign(X,Y,Z,ID): edgepositions(Direction, X,Y,Z), "
            "not match(minusy, filled, ID), category(ID, Category), not overrideempty(Category)}."
        )
        super().__init__([
            add_exception,
            block_floor_is_filled,
                          ])
