%------------------------------------%
% Shape to side LOGIC                %
%----------------------------------- %

% blobtoside (blob=shape) controls whether a blob of a certain type needs to be
% at the edgepositions of the solution given by Direction
:-
  false,
  blobtoside(Type, Category, Direction),
  category(ID1, Category),
  assign(X1, Y1, Z1, ID1, _,_,_),
  not cellboundary(Direction, X1, Y1, Z1),
  cellboundary(Direction, X2, Y2, Z2),
  originconnected(Type, X1, Y1, Z1).
  %originconnected(Type, X2, Y2, Z2).

simpleallconnected(Type) :- blobtoside(Type, Category, _), false.

% with blobtoside all tiles that connect at the side are connected with each other
originconnected(Type, X1, Y1, Z1) :-
false,
  blobtoside(Type, Category, Direction),
  cellboundary(Direction, X1, Y1, Z1).


  %not 1 {assign(X2, Y2, Z2, ID2, _,_,_): cellboundary(Direction, X2, Y2, Z2),
  %oconnected(Type, Category, X1, Y1, Z1, X2, Y2, Z2)}.
