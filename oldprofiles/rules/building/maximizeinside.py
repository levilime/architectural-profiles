from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class MaximizeInside(DeclarativeConstraints):

    def __init__(self):
        maximize_inside = DeclarativeConstraint(
            "Have as much inside as possible.",
            "#maximize {Y@1, X: assign(_,_,_, X), category(X, inside), textureswithtag(void, Y)}."
        )
        super().__init__([maximize_inside])