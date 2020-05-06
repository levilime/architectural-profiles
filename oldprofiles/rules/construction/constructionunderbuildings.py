from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class ConstructionUnderBuildings(DeclarativeConstraints):

    def __init__(self):
        dont_use_foundation_tiles = DeclarativeConstraint(
            "Don't use foundation tiles",
            ":- assign(_, _, _, ID), category(ID, foundation).\n"
        )

        no_roof_directly_above_construction = DeclarativeConstraint(
            "no roof directly above construction",
            ":- assign(_, Y, _, ID1), assign(_, Y + 1, _, ID2), category(ID1, construction), category(ID2, roof).\n"
        )

        building_must_either_be_on_ground_or_under_a_supporting_construction = DeclarativeConstraint(
            "Building must either be on ground or under a supporting construction.",
            ""
            "supportcategories(building).supportcategories(construction).\n"
            "supported(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, filled).\n"
            "supported(X,Y,Z) :- metaposition(minusy), assign(X,Y,Z, ID), Y = 0, category(ID, Category), supportcategories(Category).\n"
            "supported(X,Y,Z) :- not metaposition(minusy), boundarymatchobjective(EdgeD, X,Y,Z, EdgeID), \n"
            "category(EdgeID, C), supportcategories(C).\n"
            "supported(X,Y,Z) :- assign(X,Y,Z, ID), Y > 0, category(ID, Category), supportcategories(Category),"
            " supported(X, Y-1,Z).\n"
            ":- 1 {assign(X,Y,Z,ID): category(ID, building), not supported(X,Y,Z)}.\n"
        )
        support_construction_always_transitively_underneath_building = DeclarativeConstraint(
            "Support always transitively underneath a building.",
            ""
            "issupporting(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, building).\n"
            "issupporting(X,Y,Z) :- not metaposition(y), assign(X,Y,Z, ID), category(ID, construction), Y >= ysize.\n"
            "issupporting(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, construction), issupporting(X,Y+1,Z).\n"
            ":- 1 {assign(X,Y,Z,ID): category(ID, construction), not issupporting(X,Y,Z)}.\n"
        )

        super().__init__([dont_use_foundation_tiles,
                          building_must_either_be_on_ground_or_under_a_supporting_construction,
                          support_construction_always_transitively_underneath_building,
                          no_roof_directly_above_construction
                          ])
