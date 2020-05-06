from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class HousesPeriphery(DeclarativeConstraints):

    def __init__(self):

        building_should_not_have_other_building_in_edge = DeclarativeConstraint(
            "No building in edge of other building.",
            ":-  assign(X1,Y1,Z1,ID1), category(ID1, corner), category(ID1, interior), \n"
            "1 {assign(X2, Y1, Z1, ID2): adjacent(X1, Y1, Z1, X2, Y1, Z1), texture(ID2, _ ,_ ,_ ,_,_ ,_), category(ID2, interior)}, \n"
            "1 {assign(X1, Y1, Z2, ID3): adjacent(X1, Y1, Z1, X1, Y1, Z2), texture(ID3, _ ,_ ,_ ,_,_ ,_), category(ID3, interior)}, \n"
            "assign(X2, Y1, Z2, ID4), not category(ID4, interior)."
        )

        super().__init__([building_should_not_have_other_building_in_edge
                          ])
