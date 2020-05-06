from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class FilledConnectedBuildings(DeclarativeConstraints):

    def __init__(self):
        buildings_directly_connected_to_filled = DeclarativeConstraint(
        "Buildings can only be built if connected to filled.",
            "supportcategories(building).supportcategories(interior).\n"
            "supported(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, filled).\n"
            "supported(X,Y,Z, D) :- direction(D), assign(X,Y,Z, ID), category(ID, filled).\n"            
            
            "supported(X,Y,Z) :- assign(X,Y,Z, ID),  category(ID, Category), supportcategories(Category),"
            "directionmap(D, X,Y,Z, X1, Y1, Z1), supported(X1, Y1, Z1, D).\n"
            
            "supported(X,Y,Z, D) :- assign(X,Y,Z, ID),  category(ID, Category), supportcategories(Category),"
            "directionmap(D, X,Y,Z, X1, Y1, Z1), supported(X1, Y1, Z1, D).\n"
            
            ":- 1 {assign(X,Y,Z,ID): category(ID, building), not supported(X,Y,Z)}.\n"
        )
        super().__init__([
            buildings_directly_connected_to_filled
                          ])
