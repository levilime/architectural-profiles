from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class MountainousTerrain(DeclarativeConstraints):

    def __init__(self):
        if_filled_then_all_underneath_must_be_filled = DeclarativeConstraint(
            "Filled all underneath must be filled.",
            ":- adjacent(X1, Y1, Z1, X1, Y2, Z1), Y1 > 0,Y2 = Y1 - 1,assign(X1, Y1, Z1, ID1),category(ID1, filled),\n"
            "assign(X1, Y2, Z1, ID2), not category(ID2, filled)."
        )

        filled_may_only_grow_by_one = DeclarativeConstraint(
            "Filled may only grow by one vertically.",
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), category(ID1, filled),\n"
            "Y1 = ysize,  \n"
            "YX2 > Y1 + 1, assign(X2, YX2, Z2, ID2), category(ID2, filled). \n"
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), category(ID1, filled),\n"
            "Y1 = ysize,  \n"
            "YX2 < Y1 - 1, assign(X2, YX2, Z2, ID2), category(ID2, filled). \n"
            
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), category(ID1, filled),\n"
            "assign(X1, Y1+1, Z1, IDX), not category(IDX, filled),  \n"
            "YX2 > Y1 + 1, assign(X2, YX2, Z2, ID2), category(ID2, filled). \n"
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), category(ID1, filled),\n"
            "assign(X1, Y1+1, Z1, IDX), not category(IDX, filled),  \n"
            "YX2 < Y1 - 1, assign(X2, YX2, Z2, ID2), category(ID2, filled). \n"
        )

        buildings_may_not_be_built_on_air = DeclarativeConstraint(
            "Buildings may not be built on air.",
            ":- assign(X1,Y1,Z1, ID1), category(ID1, building), assign(X1, Y1 - 1, Z1, ID2), \n"
            "category(ID2, void)."
        )



        super().__init__([if_filled_then_all_underneath_must_be_filled,
                          # filled_may_only_grow_by_one,
                          # there_must_be_place_where_no_filled,
                          # buildings_may_not_be_built_on_air
                          ])

