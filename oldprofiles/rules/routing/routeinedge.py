from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class RouteInEdge(DeclarativeConstraints):

    def __init__(self):
        horizontal_edge_connection = DeclarativeConstraint(
        "With every 'adjacentblockneighbor(Direction)' added, a straight path should exist in that edge."
        "Needs connectroomsandpaths to work.",
        ":- adjacentblockneighbor(x), \n"
        "not 1 {assign(X,Y,Z,ID): cell(X,Y,Z), category(ID, path), X = xsize, routedirection(ID, x)}.\n\n"
        ":- adjacentblockneighbor(minusx),\n"
        "not 1 {assign(X,Y,Z,ID): cell(X,Y,Z), category(ID, path), X = 0, routedirection(ID, minusx)}.\n\n"
        ":- adjacentblockneighbor(z), \n"
        "not 1 {assign(X,Y,Z,ID): cell(X,Y,Z), category(ID, path), Z = zsize, routedirection(ID, z)}.\n\n"
        ":- adjacentblockneighbor(minusz),\n"
        "not 1 {assign(X,Y,Z,ID): cell(X,Y,Z), category(ID, path), Z = 0, routedirection(ID, minusz)}.\n\n"
        )

        vertical_edge_connection = DeclarativeConstraint(
        "With every vertical 'adjacentblockneighbor(Direction)' added, stairs should exist in that edge."
        "Needs connectroomsandpaths to work.",
        ":- adjacentblockneighbor(y), \n"
        "not 1 {assign(X,Y,Z,ID): cell(X,Y,Z), texturegroup(ID, stairs), Y = ysize, routedirection(ID, y), X > 0, X < xsize - 1,Z > 0, Z < zsize - 1}.\n"
        ":- adjacentblockneighbor(minusy),\n"
        "not 1 {assign(X,Y,Z,ID): cell(X,Y,Z), texturegroup(ID, stairs_above_connector), Y = 0, routedirection(ID, minusy)}.\n\n"
        "% dissallow building stairs on the edges because it may not be possible to connect the stairs on the next level\n"
        ":- 1 {assign(X,Y,Z,ID): cell(X,Y,Z), not X = 0, not X=xsize, not Z = 0, not Z = zsize, texturegroup(ID, stairs_above_connector), routedirection(ID, minusy)}.\n"
        ":- 1 {assign(X,Y,Z,ID): cell(X,Y,Z), not X = 0, not X=xsize, not Z = 0, not Z = zsize, texturegroup(ID, stairs), routedirection(ID, y)}.\n"
        "\n"
        )
        super().__init__([
            horizontal_edge_connection,
            # vertical_edge_connection
                          ])
