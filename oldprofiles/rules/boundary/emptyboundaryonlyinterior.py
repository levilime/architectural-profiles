

from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class ExemptAllBoundaryExceptInterior(DeclarativeConstraints):

    def __init__(self):
        exempt_all_except_interior = DeclarativeConstraint(
         "ignore all except interior.",
         "overrideempty(A) :- texture(ID, _, _ ,_ , _, _ ,_ ), category(ID, A), not category(ID, interior)."
        )
        super().__init__([exempt_all_except_interior])
