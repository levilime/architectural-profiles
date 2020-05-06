from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class GetStraightTerrain(DeclarativeConstraints):

    def __init__(self):
        # TODO get the average of the filled height instead of lowest
        straight_terrain = DeclarativeConstraint(
            "Straighten the terrain.",
            ":- assign(X1, Y1, Z1, ID1), adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X2, Y2, Z2, ID1), \n"
            "category(ID1, filled), category(ID2, filled), not Y1 = Y2.\n"
            # ":- assign(X1, Y1, Z1, ID1), category(ID1, filled), averageheightfilled(C), Y1 > C."
            ":- assign(X1, Y1, Z1, ID1), not category(ID1, filled), overridefilled(X, Y, Z), Y1 < Y."

            # "averageheightfilled(A) :- ...

            # "averageheightfilled(C) :- A = #sum{Y: assign(X,Y,Z,ID), overridefilled(X,Y,Z), \n"
            # "texture(ID, _, _, _, _, _, _), category(ID, filled)},\n"
            # "B = #count{X,Y,Z: overridefilled(X,Y,Z), assign(X,Y,Z,ID), texture(ID, _, _, _, _, _, _), "
            # "category(ID, filled)}, C = A / B.\n"
        )
        super().__init__([straight_terrain])
