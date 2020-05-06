from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class PathToEmptyEdge(DeclarativeConstraints):

    def __init__(self):
        riding_the_sunset = DeclarativeConstraint(
            "Paths that move towards an empty edge are seen as connected. It hints to a world beyond what is computed...",
            "isconnected(X,Y,Z) :- assign(X,Y,Z, ID), routedirection(ID, Direction), edgepositions(Direction, X,Y,Z).\n"
        )
        super().__init__([riding_the_sunset])