from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint


class ConnectRoomsAndPaths(DeclarativeConstraints):

    def __init__(self):
        adjacent_route_connected = DeclarativeConstraint(
            "Give minecraft pathway tiles, routing semantics.",
            "connectedroute(X1, Y1, Z1, X2, Y2, Z2) :- assign(X1, Y1, Z1, ID1), routedirection(ID1, Direction),\n"
            "directionmap(Direction, X1, Y1, Z1, X2, Y2, Z2)."
        )

        needs_to_be_traversable = DeclarativeConstraint(
            "Whether two adjacent tiles need to be traversable.",
            "requiredtraversable(ID1, ID2):- category(ID1, routing), category(ID1, outside), \n"
            "category(ID2, routing), category(ID2, outside).\n"
            "requiredtraversable(ID1, ID2):- category(ID1, routing), category(ID1, interior), \n"
            "category(ID2, routing), category(ID2, interior).\n"
            "requiredtraversable(ID1, ID2):- category(ID1, door), \n"
            "category(ID2, routing).\n"
            "requiredtraversable(ID1, ID2):- category(ID1, routing), category(ID1, outside), \n"
            "category(ID2, routing), category(ID2, interior).\n"
            "requiredtraversable(ID2, ID1):- category(ID1, routing), category(ID1, outside), \n"
            "category(ID2, routing), category(ID2, interior).\n"
        )

        path_may_only_exist_if_connected_transitively_with_a_door = DeclarativeConstraint(
            "Path may only exist if (transitively) connected with a door.",
            "isconnected(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, door), category(ID, boundary).\n"
            "isconnected(X1,Y1,Z1) :- assign(X1,Y1,Z1,ID), category(ID, routing), category(ID, outside), \n"
            "adjacent(X1,Y1,Z1, X2, Y2, Z2), connectedroute(X1,Y1, Z1, X2, Y2, Z2), isconnected(X2,Y2,Z2).\n"
            "1 {cell(X1, Y1, Z1): isconnected(X1, Y1, Z1)} :- assign(X1, Y1, Z1, ID1), category(ID1, outside), category(ID1, routing).\n"
        )

        stairs_goes_somewhere_two_directions = DeclarativeConstraint(
            "Stairs should go somewhere, two directions. Specified IsConnected version that goes a certain direction.",
            "isconnected(X,Y,Z, D) :- direction(D), assign(X,Y,Z, ID), category(ID, door), category(ID, boundary).\n"
            "isconnected(X,Y,Z, D) :- direction(D), assign(X,Y,Z, ID), category(ID, stairs).\n"
            "isconnected(X,Y,Z, D) :- direction(D), assign(X,Y,Z,ID), routedirection(ID, D), category(ID, routing), \n"
            "directionmap(D1, X,Y,Z, X1, Y1, Z1), assign(X1, Y1, Z1, ID1), routedirection(ID1, D1),\n"
            "not oppositedirection(D, D1), isconnected(X1, Y1, Z1, D1).\n"
            "doestraversing(X,Y,Z) :- direction(D1), direction(D2), not D1 = D2, directionmap(D1, X,Y,Z, X1, Y1, Z1),\n"
            "directionmap(D2, X,Y,Z, X2, Y2, Z2), isconnected(X, Y, Z, D1), isconnected(X, Y, Z, D2),\n"
            " assign(X,Y,Z, ID), routedirection(ID, D1), routedirection(ID, D2).\n"
            "1 {cell(X1, Y1, Z1): doestraversing(X1, Y1, Z1)} :- assign(X1, Y1, Z1, ID1), category(ID1, stairs).\n"
        )

        pathway_tiles_only_connect_when_routing_connects = DeclarativeConstraint(
            "Require tiles to be connected through traversal.",
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2),assign(X1, Y1, Z1, ID1), assign(X2, Y2, Z2, ID2), % not adjacenttoneighboredge(X1,Y1,Z1),\n"
            "not category(ID1, optionalrouting), not category(ID2, optionalrouting),\n"
            "requiredtraversable(ID1, ID2), requiredtraversable(ID2, ID1), not connectedroute(X1, Y1, Z1, X2, Y2, Z2).\n"
        )

        stairs_do_not_go_directly_into_doors = DeclarativeConstraint(
            "Stairs do not directly move in doors. First rule for bottom of stairs, second for top.",
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), directionmap(D2, X2, Y2, Z2, X1, Y1, Z1), routedirection(ID1, D2),\n"
            "assign(X1, Y1, Z1, ID1), \n"
            "assign(X2, Y2, Z2, ID2), category(ID1, door), category(ID2, stairs).\n"
            ":- adjacent(X1, Y1, Z1, X2, Y2, Z2), directionmap(D1, X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1),\n"
            "assign(X2, Y2, Z2, ID2), \n"
            "texturegroup(ID1, stairs_above_connector), category(ID2, door), \n"
            "routedirection(ID1, D1).\n"
        )

        all_paths_must_be_connected_with_each_other = DeclarativeConstraint(
            "All paths must be connected to each other",
            ":- assign(X1,Y1,Z1,ID1), category(ID1, outside), category(ID1, routing),\n"
            "not 1 {assign(X2, Y2, Z2, ID2): category(ID1, outside), category(ID1, routing),\n"
            "connectedroute(X1, Y1, Z1, X2, Y2, Z2)}.\n"
        )
        super().__init__([
                          adjacent_route_connected,
                          needs_to_be_traversable,
                          path_may_only_exist_if_connected_transitively_with_a_door,
                          pathway_tiles_only_connect_when_routing_connects,
                          all_paths_must_be_connected_with_each_other,
                          # stairs_goes_somewhere_two_directions,
                          stairs_do_not_go_directly_into_doors
                          ])
