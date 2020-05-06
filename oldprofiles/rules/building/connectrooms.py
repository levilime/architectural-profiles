from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class ConnectRooms(DeclarativeConstraints):

    def __init__(self):
        inside_directly_connected_to_door = DeclarativeConstraint(
            "Every space inside is either directly or transitively connected with a door.",
            "goesoutside(X1, Y1, Z1):- assign(X1, Y1, Z1, ID1), category(ID1, door), category(ID1, boundary), \n"
            "connectedroute(X1,Y1, Z1, X2, Y2, Z2), assign(X2, Y2, Z2, ID2), category(ID2, routing), category(ID2, outside).\n"
            
            "goesoutside(X1, Y1, Z1):- assign(X1, Y1, Z1, ID1), category(ID1, building), \n"
            "category(ID1, interior), \n"  # ; category(ID1, inside)
            "adjacent(X1,Y1,Z1, X2, Y2, Z2), connectedroute(X1,Y1, Z1, X2, Y2, Z2), \n"
            "goesoutside(X2,Y2,Z2). \n"
            "goesoutside(X1, Y1, Z1):- assign(X1, Y1, Z1, ID1), category(ID1, building), \n"
            "category(ID1, inside), \n"  # ; category(ID1, inside)
            "adjacent(X1,Y1,Z1, X2, Y2, Z2), connectedroute(X1,Y1, Z1, X2, Y2, Z2), \n"
            "goesoutside(X2,Y2,Z2). \n"

            "1 {cell(X, Y, Z): goesoutside(X, Y, Z)} :-  assign(X, Y, Z, ID), \n"
            " category(ID, building),"
            " category(ID, interior).\n"
            "1 {cell(X, Y, Z): goesoutside(X, Y, Z)} :-  assign(X, Y, Z, ID), \n"
            " category(ID, building),"
            " category(ID, inside)."
        )

        super().__init__([inside_directly_connected_to_door
                          ])
