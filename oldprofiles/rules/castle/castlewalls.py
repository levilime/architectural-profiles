from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class CastleWalls(DeclarativeConstraints):

    def __init__(self):
        castle_walls_may_not_float = DeclarativeConstraint(
            "Castle walls may not float.",
            ""
            "castlecategories(fortified).\n"
            "castlesupported(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, filled).\n"
            "castlesupported(X,Y,Z) :- assign(X,Y,Z, ID), Y = 0, category(ID, Category), castlecategories(Category).\n"
            "castlesupported(X,Y,Z) :- assign(X,Y,Z, ID), Y > 0, category(ID, Category), castlecategories(Category),"
            " castlesupported(X, Y-1,Z).\n"
            ":- 1 {assign(X,Y,Z,ID): category(ID, Category), castlecategories(Category),  not castlesupported(X,Y,Z)}.\n"
        )

        super().__init__([castle_walls_may_not_float
                          ])
