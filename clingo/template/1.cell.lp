%------------------------------------%
% CELL LOGIC                         %
%----------------------------------- %

#const rxMax = 0.
#const ryMax = 3.
#const rzMax = 0.
%cell(minusxsize..xsize, minusysize..ysize, minuszsize..zsize).
%currentblock(minusxsize..xsize, minusysize..ysize, minuszsize..zsize).

% rotational assignments
rxA(0..rxMax). ryA(0..ryMax). rzA(0..rzMax).
% additional cells of surrounding blocks

rot(Rot) :- Rot = (Rx, Ry, Rz), rxA(Rx), ryA(Ry), rzA(Rz).

cell(P) :- P = (X,Y,Z), cell(X,Y,Z).

% current block + one cell padding around.
paddedcurrentblock(I, X,Y,Z) :-
   currentblock(I, X1,Y1,Z1),
   cell(X2,Y2,Z2),
   |X2 - X1| <= 1, |Y2 - Y1| <= 1, |Z2 - Z1| <= 1, cell(X,Y,Z).
paddedcurrentblock(I, X,Y,Z) :- currentblock(I, X,Y,Z).

% edge positions denote the boundary positions of a currentblock
edgepositions(x, X,Y,Z, I) :-
   cell(X,Y,Z),
   currentblock(I, X,Y,Z),
   X = xsize.
edgepositions(minusx, X,Y,Z, I) :-
   cell(X,Y,Z),
   currentblock(I, X,Y,Z),
   X = 0.
edgepositions(y, X,Y,Z, I) :-
   cell(X,Y,Z),
   currentblock(I, X,Y,Z),
   Y = ysize.
edgepositions(minusy, X,Y,Z, I) :-
   cell(X,Y,Z),
   currentblock(I, X,Y,Z),
   Y = 0.
edgepositions(z, X,Y,Z, I) :-
   cell(X,Y,Z),
   currentblock(I, X,Y,Z),
   Z = zsize.
edgepositions(minusz, X,Y,Z, I) :-
   cell(X,Y,Z),
   currentblock(I, X,Y,Z),
   Z = 0.

% cellboundary denotes the boundaries of the solution
cellboundary(X,Y,Z) :- cellboundary(minusx, X,Y,Z).
cellboundary(X,Y,Z) :- cellboundary(minusy, X,Y,Z).
cellboundary(X,Y,Z) :- cellboundary(minusz, X,Y,Z).
cellboundary(X,Y,Z) :- cellboundary(x, X,Y,Z).
cellboundary(X,Y,Z) :- cellboundary(y, X,Y,Z).
cellboundary(X,Y,Z) :- cellboundary(z, X,Y,Z).

% cellboundary denotes the boundaries of the solution
cellboundary(minusx, X,Y,Z) :-
  cell(X,Y,Z),
  X = #min{MinX: cell(MinX, _, _)}.
cellboundary(minusy, X,Y,Z) :-
  cell(X,Y,Z),
  Y = #min{MinY: cell(_, MinY, _)}.
cellboundary(minusz, X,Y,Z) :-
  cell(X,Y,Z),
  Z = #min{MinZ: cell(_, _, MinZ)}.
cellboundary(x, X,Y,Z) :-
  cell(X,Y,Z),
  X = #max{MaxX: cell(MaxX, _, _)}.
cellboundary(y, X,Y,Z) :-
  cell(X,Y,Z),
  Y = #max{MaxY: cell(_, MaxY, _)}.
cellboundary(z, X,Y,Z) :-
  cell(X,Y,Z),
  Z = #max{MaxZ: cell(_, _, MaxZ)}.

% cell goes outside is true for those cells that are at the boundary of a currentblock,
% but are adjacent to a new block that will be generated in a later solving iteration step.
cellgoesoutside(X,Y,Z) :-
  metaposition(I, Direction),
  edgepositions(Direction, X, Y, Z, I).

% this rule is created so that if there are no adjacentblockneighbors then all sides have the cutoffexception
adjacentblockneighbor(I, undefined) :- currentblock(I, _, _, _).
