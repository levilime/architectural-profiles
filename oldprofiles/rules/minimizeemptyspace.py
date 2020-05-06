from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class MinimizeEmptySpace(DeclarativeConstraints):

    def __init__(self):
        minimize_empty_space = DeclarativeConstraint(
            "Minimize empty space.",
            "%#minimize { C@1,_: C = #count{I: assign(_,_,_,I), category(I, void)}.\n" +
            "%:~ assign(_,_,_,I), category(I, void)\n" +
            "#minimize {Y@1, X: assign(_,_,_, X), category(X, void), textureswithtag(void, Y)}."
        )
        super().__init__([minimize_empty_space])