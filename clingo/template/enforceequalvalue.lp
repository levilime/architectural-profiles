%------------------------------------%
% equalvalue LOGIC                   %

% Enforce that two cells that should have the same tile,
% actually have the same tile.

%----------------------------------- %

%@toggle
:-
  equalvalue(X1, Y1, Z1, X2, Y2, Z2),
  assign(X1, Y1, Z1, ID, Rx, Ry, Rz),
  not assign(X2, Y2, Z2, ID, Rx, Ry, Rz).
