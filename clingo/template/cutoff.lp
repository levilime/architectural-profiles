%------------------------------------%
% Cutoff (closed) LOGIC              %

% controls whether a tile must be closed to the
% edge of the input space

%----------------------------------- %

% minusy of a bottom block is now never cutoff. This presumes that the bottom is the ground.
cutoffexception(minusy).

% cellboundary(Direction, X1, Y1, Z1, I)
:-
  metaposition(I, Direction),
  cellboundary(Direction, X1, Y1, Z1),
  cutoffside(I, Direction),
  currentblock(I, X1, Y1, Z1),
  category(ID1, Category),
  cutoff(Type, Category),
  % category(ID2, void),
  assign(X1, Y1, Z1, ID1, _,_,_),
  not cutoffmatch(Type, Direction, X1, Y1, Z1).

% this rule deduces the cutoffsides. Meaning where the block is cutoff(the edge of the solution space).
cutoffside(I, OtherDimension) :-
  direction(OtherDimension),
  not 1 {adjacentblockneighbor(I, Dimension): Dimension = OtherDimension},
  not 1 {cutoffexception(Dimension): Dimension = OtherDimension},
  currentblock(I,_,_,_).

cutoffmatch(Type, Direction, X, Y, Z) :-
  cellboundary(Direction, X, Y, Z),
  currentblock(_, X,Y,Z),
  cutoffside(Direction),
  assign(X, Y, Z, ID, Rx,Ry,Rz), %tile(ID2), not ID2 = void,
  % it is correct to not choose to move in the direction of the cutoff
  match(strict, Direction, ID, void, Rx, Ry, Rz, 0 ,_ ,0),
  % not tiledirection(Type, ID, (Rx, Ry, Rz), Direction),
  connectivitytype(Type).

cutoffmatchonlytype(Type, Direction, X, Y, Z) :-
  cellboundary(Direction, X, Y, Z),
  currentblock(_, X,Y,Z),
  cutoffside(Direction),
  assign(X, Y, Z, ID, Rx,Ry,Rz), %tile(ID2), not ID2 = void,
  not tiledirection(Type, ID, (Rx, Ry, Rz), Direction),
  connectivitytype(Type).
