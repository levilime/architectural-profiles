%------------------------------------%
% ADJACENCY LOGIC                    %
%----------------------------------- %

% every assignment must adhere to hard constraints of its neighbors
% with currentblock:
% one of the tiles being matched needs to be in this block, the other may be in this block or another block
adjacencymatchmode :- tilesolvingmode.
adjacencymatchmode :- shapegeneratormode.
adjacencymatchmode :- shapesolvingmode.

:- adjacent(X1, Y1, Z1, X2, Y2, Z2),
    directionmap(D, X1, Y1, Z1, X2, Y2, Z2),
    assign(X1, Y1, Z1, ID1, RX1, RY1, RZ1),
    currentblock(_, X1, Y1, Z1),
    not 1 {assign(X2, Y2, Z2, ID2, RX2, RY2, RZ2):
      match(strict, D, ID1, ID2, RX1, RY1, RZ1, RX2, RY2, RZ2)}
      %match(strict, (X1, Y1, Z1), (X2, Y2, Z2))}
    ,adjacencymatchmode.

% direction rotations
dir(x, 0, 1, 0, minusz).
dir(minusz, 0, 1, 0, minusx).
dir(minusx, 0, 1, 0, z).
dir(z, 0, 1, 0, x).
dir(y, 0, 1, 0, y).
dir(minusy, 0, 1, 0, minusy).

dir(D2, 0, -1, 0, D1) :-
  dir(D1, 0, 1, 0, D2),
  direction(D1),
  direction(D2).
dir(D1, 0, 0, 0, D2) :-
  D1 = D2,
  direction(D1),
  direction(D2).

dir(D1, 0, N, 0, D2) :-
  N > 0, num4(N),
  dir(D1, 0, 1, 0, DB),
  dir(DB, 0, N - 1, 0, D2).
dir(D1, 0, N, 0, D2) :-
  N < 0, num4(N),
  dir(D1, 0, -1, 0, DB),
  dir(DB, 0, N + 1, 0, D2).

num4(-8..8).
mod4(N, M) :- N >= 0, M = N \ 4, num4(N), num4(M).
mod4(N, M) :- N < 0, M = 4 - (N * -1), num4(N), num4(M).
% usage: a(-1, M) :- mod4(-1, M). (returns a(-1, 3))

sin(0,0).
sin(1,1).
sin(2,0).
sin(3,-1).
sin(N,M):- mod4(N,R), sin(R,M), num4(M).
cos(N,M) :- sin(N+1, M),  num4(M).

% whether to cell positions are the same.
equalposition(X1, Y1, Z1, X2, Y2, Z2) :- X1 = X2, Y1 = Y2, Z1 = Z2,
cell(X1, Y1, Z1), cell(X2, Y2, Z2).

% directions, the assumption is that the cells and blocks are 3dimensional boxes
direction(x).
direction(y).
direction(z).
direction(minusx).
direction(minusy).
direction(minusz).

% opposite directions
oppositedirection(x, minusx).
oppositedirection(minusx, x).
oppositedirection(y, minusy).
oppositedirection(minusy, y).
oppositedirection(z, minusz).
oppositedirection(minusz, z).

% annotation on adjacencies, if the cells are adjacent, on what side.
% meaning if X2, Y2, Z2 is on the right side of X1,Y1,Z1 then the direction is x
directionmap(x, X1, Y1, Z1, X2, Y2, Z2) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2),
  X2 = X1 + 1,
  Y2 = Y1,
  Z2 = Z1.
directionmap(minusx, X1, Y1, Z1, X2, Y2, Z2) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2),
  X2 = X1 - 1,
  Y2 = Y1,
  Z2 = Z1.
directionmap(z, X1, Y1, Z1, X2, Y2, Z2) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2),
  X2 = X1,
  Y2 = Y1,
  Z2 = Z1 + 1.
directionmap(minusz, X1, Y1, Z1, X2, Y2, Z2) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2),
  X2 = X1,
  Y2 = Y1,
  Z2 = Z1 - 1.
directionmap(y, X1, Y1, Z1, X2, Y2, Z2) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2),
  X2 = X1,
  Y2 = Y1 + 1,
  Z2 = Z1.
directionmap(minusy, X1, Y1, Z1, X2, Y2, Z2) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2),
  X2 = X1,
  Y2 = Y1 - 1,
  Z2 = Z1.

% adjacent means that two cells are next to each other
adjacent(X1, Y1, Z1, X2, Y2, Z2) :-
  cell(X1, Y1, Z1),
  cell(X2, Y2, Z2),
  |X1 - X2| == 1,
  |Y1 - Y2| == 0,
  |Z1 - Z2| == 0.
adjacent(X1, Y1, Z1, X2, Y2, Z2) :-
  cell(X1, Y1, Z1),
  cell(X2, Y2, Z2),
  |X1 - X2| == 0,
  |Y1 - Y2| == 1,
  |Z1 - Z2| == 0.
adjacent(X1, Y1, Z1, X2, Y2, Z2) :-
  cell(X1, Y1, Z1),
  cell(X2, Y2, Z2),
  |X1 - X2| == 0,
  |Y1 - Y2| == 0,
  |Z1 - Z2| == 1.

adjacent((X1, Y1, Z1), (X2, Y2, Z2)) :-
  adjacent(X1, Y1, Z1, X2, Y2, Z2).

% match if tile A at one side fits with tile B on the opposite side of B.
match(Type, D, ID1, ID2, 0, RY1, 0, 0, RY2,0) :-
  mod4(RY2 - RY1, RDiff),
  dir(D, 0, -RY1, 0, Dn),
  adjacency(Type, ID1, ID2, Dn, 0, RDiff, 0), ryA(RY1), ryA(RY2)
% TODO insert again when ready, also the adjacency oppositely should exist
%, oppositedirection(Dn, Dopposite),
%adjacency(Type, ID2, ID1, Dopposite, 0, RDiff, 0)
.

match(Type, P1, P2) :-
false,
P1 = (X1,Y1,Z1),
P2 = (X2, Y2, Z2),
adjacent(P1, P2),
assign(X1, Y1, Z1, ID1, RX1, RY1, RZ1),
assign(X2, Y2, Z2, ID2, RX2, RY2, RZ2),
directionmap(D, X1, Y1, Z1, X2, Y2, Z2),
match(Type, D, ID1, ID2, 0, RY1, 0, 0, RY2,0).
% adjacency(Type, ID1, ID2, D, RX1, RY1, RZ1).

% tile directions denote for a tile at a certain position what directions it
% connects to according to the given adjacency type.
%tiledirections(Type, X,Y,Z, ID1, Ry, D) :-
%  connectivitytype(Type),
%  assign(X,Y,Z, ID1, 0, Ry, 0),
%  tile(ID1),
%  tile(ID2),
%  not ID2 = void,
%  match(Type, D, ID1, ID2, 0, Ry, 0, 0, _, 0),
%  ryA(Ry).

tiledirection(Type, ID, Rot, D) :-
  tiledirection(ID, Type, Dir),
  Rot = (Rx, Ry, Rz),
  rxA(Rx), ryA(Ry), rzA(Rz),
  dir(Dir, Rx, Ry, Rz, D).

% if a entrancedirection is defined than it has a tiledirection as well
tiledirection(Type, ID, Rot, D) :-
  entrancedirection(Type, ID, Rot, D).

entrancedirection(Type, ID, Rot, D) :-
  tileentrance(ID, Type, Dir),
  Rot = (Rx, Ry, Rz),
  rxA(Rx), ryA(Ry), rzA(Rz),
  dir(Dir, Rx, Ry, Rz, D).

equivalenttiledirectionrotation(ID, R1, R2) :-
  tile(ID),
  rxA(Rx1), ryA(Ry1), rzA(Rz1),
  rxA(Rx2), ryA(Ry2), rzA(Rz2),
  R1 = (Rx1, Ry1, Rz1),
  R2 = (Rx2, Ry2, Rz2),
  not 1 {
    not tiledirection(Type, ID, R1, D):
    tiledirection(Type, ID, R2, D),
     alltypes(Type)}.

equivalententrancedirectionrotation(ID, R1, R2) :-
  tile(ID),
  rxA(Rx1), ryA(Ry1), rzA(Rz1),
  rxA(Rx2), ryA(Ry2), rzA(Rz2),
  R1 = (Rx1, Ry1, Rz1),
  R2 = (Rx2, Ry2, Rz2),
  not 1 {
    not entrancedirection(Type, ID, R1, D):
    entrancedirection(Type, ID, R2, D),
    alltypes(Type)}.
