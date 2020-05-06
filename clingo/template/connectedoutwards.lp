%------------------------------------%
% CONNECTEDOUTWARDS LOGIC            %

% when a cell is connectedoutwards, it has an subtype adjacency,
% towards the outside.
% connectedoutwards allows for shapes and connectivities to
% express that the connectivity may be resolved in a future solved block

%----------------------------------- %

% connectedoutwards decides whether a cell is connected with an outside edge
% for any category
connectedoutwards(Type, X1, Y1, Z1) :-
  cellboundary(Direction, X1, Y1, Z1),
  connectivitytype(Type),
  assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
  match(Type, Direction, ID1, _, Rx1, Ry1, Rz1, _, _, _).
  %tiledirection(Type, ID1, (Rx1, Ry1, Rz1), Direction).
% transative
connectedoutwards(Type, X1, Y1, Z1) :-
  oconnected(Type, X1, Y1, Z1, X2, Y2, Z2),
  connectedoutwards(Type, X2, Y2, Z2).
% for a specific category
connectedoutwards(Type, Category, X1, Y1, Z1) :-
  cellboundary(Direction, X1, Y1, Z1),
  connectivitytype(Type),
  assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
  match(Type, Direction, ID1, _, Rx1, Ry1, Rz1, _, _, _),
  %tiledirection(Type, ID1, (Rx1, Ry1, Rz1), Direction),
  category(ID1, Category).
% transative
connectedoutwards(Type, Category, X1, Y1, Z1) :-
  oconnected(Type, Category, X1, Y1, Z1, X2, Y2, Z2),
  connectedoutwards(Type, Category, X2, Y2, Z2).
