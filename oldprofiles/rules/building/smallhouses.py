from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class SmallHouses(DeclarativeConstraints):

    def __init__(self):
        no_adjacent_inside_tile_not_vertical = DeclarativeConstraint(
            "Keep houses small by having no horizontally adjacent inside tiles.",
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), assign(X2, Y2, Z2, ID2), Y1 = Y2, \n"
            "category(ID1, inside), category(ID2, inside)."
        )
        no_adjacent_inside_tile = DeclarativeConstraint(
            "Keep houses small by having no horizontally adjacent inside tiles.",
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), assign(X2, Y2, Z2, ID2), \n"
            "category(ID1, inside), category(ID2, inside)."
        )

        all_interior_tiles_need_to_be_adjacent_to_void = DeclarativeConstraint(
            "Interior tiles need to be adjacent to a void to keep the houses small.",
            "3 {assign(X2,Y1,Z2,ID2): adjacent(X1, Y1, Z1, X2, Y1, Z2), texture(ID2, _ ,_ ,_ ,_,_ ,_),"
            " not category(ID2, interior)} :- cell(X1,Y1,Z1),"
            " assign(X1,Y1,Z1,ID1), category(ID1, nook), category(ID1, interior).\n"
            "2 {assign(X2,Y1,Z2,ID2): adjacent(X1, Y1, Z1, X2, Y1, Z2), texture(ID2, _ ,_ ,_ ,_,_ ,_),"
            " not category(ID2, interior)} :- cell(X1,Y1,Z1),"
            " assign(X1,Y1,Z1,ID1), category(ID1, corner), category(ID1, interior).\n"
            "1 {assign(X2,Y1,Z2,ID2): adjacent(X1, Y1, Z1, X2, Y1, Z2),texture(ID2, _ ,_ ,_ ,_,_ ,_),"
            " not category(ID2, interior)} :- cell(X1,Y1,Z1), "
            " assign(X1,Y1,Z1,ID1), category(ID1, straight), category(ID1, interior). \n"
            ":- 1 {assign(X,Y,Z, ID):cell(X, 1, Z), texturegroup(ID, inside)}."
        )

        super().__init__([all_interior_tiles_need_to_be_adjacent_to_void
                          ])
