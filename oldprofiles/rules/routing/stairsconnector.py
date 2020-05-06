from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class StairsConnector(DeclarativeConstraints):

    def __init__(self):
        stairs_connector_only_above_stairs = DeclarativeConstraint(
        "stairsconnector may only exist above stairs.",
        ":- assign(X,Y,Z, ID), texturegroup(ID, stairs_above_connector), assign(X,Y-1,Z, ID2),"
        "not texturegroup(ID2, stairs).\n"
        )

        stairs_connector_needs_to_go_somewhere = DeclarativeConstraint(
        "stairsconnector needs to go somewhere.",
        "1 {cell(X1, Y1, Z1): directionmap(D, X1, Y1, Z1, X2, Y2, Z2), assign(X2, Y2, Z2, _)} \n"
        ":- assign(X1, Y1, Z1, ID1), texturegroup(ID1, stairs_above_connector), routedirection(ID1, D), not D = minusy."
        )

        every_stairs_needs_to_have_connector_attached = DeclarativeConstraint(
        "stairsconnector needs to go somewhere.",
        ":- assign(X,Y,Z, ID), texturegroup(ID, stairs), assign(X,Y+1,Z, ID2),"
        "not texturegroup(ID2, stairs_above_connector).\n"
        )

        stairs_not_horizontally_adjacent = DeclarativeConstraint(
        "Stairs not horizontally adjacent.",
        ":- assign(X1, Y1, Z1, ID1), texturegroup(ID1, stairs), assign(X2, Y2, Z2, ID2), texturegroup(ID2, stairs), \n"
        "Y1 = Y2, adjacent(X1, Y1, Z1, X2, Y2, Z2)."
        )

        super().__init__([
            stairs_connector_only_above_stairs,
            stairs_not_horizontally_adjacent,
            stairs_connector_needs_to_go_somewhere,
            every_stairs_needs_to_have_connector_attached
                          ])
