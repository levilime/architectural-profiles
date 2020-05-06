from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class NoTileTemplateUsage(DeclarativeConstraints):

    def __init__(self):
        dont_use_template_tile = DeclarativeConstraint(
            "dont use a tile that has the category template",
            ":- assign(X,Y,Z, ID), cell(X,Y,Z), texture(ID, _,_,_,_,_,_), category(ID, template)."
        )
        super().__init__([dont_use_template_tile])

