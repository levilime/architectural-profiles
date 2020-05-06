


 % equal tiles are connected
 %connectedthrough(Type, Category, X1, Y1, Z1, X2, Y2, Z2) :- equalposition(X1, Y1, Z1, X2, Y2, Z2),
 %relevantthroughcategory(Category),
 %assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1), assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2),
%  connectivitytype(Type).
 % directly adjacent tiles don't need through
 %connectedthrough(Type, Category, X1, Y1, Z1, X2, Y2, Z2) :- assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
 %match(Type, Dir, ID1, ID2, Rx1, Ry1, Rz1, Rx2, Ry2, Rz2), directionmap(Dir, X1, Y1, Z1, X2, Y2, Z2),
 %assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2), relevantthroughcategory(Category).

 %connectedthrough(Type, Category, X1, Y1, Z1, X2, Y2, Z2) :- assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
 %match(Type, Dir, ID1, IDN, Rx1, Ry1, Rz1, RxN, RyN, RzN), directionmap(Dir, X1, Y1, Z1, XN, YN, ZN),
 %assign(XN, YN, ZN, IDN, RxN, RyN, RzN), connectedthrough(Type, Category, XN, YN, ZN, X2, Y2, Z2),
 %connectivitytype(Type), category(IDN, Category), relevantthroughcategory(Category).



% tiles with a required distance should be connectedthrough
:- requireddistance(Type, CategoryFrom, CategoryThrough, CategoryTo, MinD, MaxD),
assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2), category(ID2, CategoryTo), category(ID1, CategoryFrom),
not 1 {connectedthrough(Type, CategoryThrough, X1, Y1, Z1, X2, Y2, Z2):
assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1), relevantthroughcategory(CategoryThrough)}.

% the distance should not be too high
:- requireddistance(Type, CategoryFrom, CategoryThrough, CategoryTo, MinD, MaxD), assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
category(ID1, CategoryFrom),
Distance = #max{D: category(ID2, CategoryTo), assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2),
  connectedthrough(Type, CategoryThrough, X1, Y1, Z1, X2, Y2, Z2), directdistance(xyz, X1, Y1, Z1, X2, Y2, Z2, D)},
Distance > MaxD.

% the distance should not be too low
:- requireddistance(Type, CategoryFrom, CategoryThrough, CategoryTo, MinD, MaxD), assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
category(ID1, CategoryFrom), connectedthrough(Type, CategoryThrough, X1, Y1, Z1, X2, Y2, Z2),
% max distance from end point
Distance = #max{D: category(ID2, CategoryTo), assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2),
  connectedthrough(Type, CategoryThrough, X1, Y1, Z1, X2, Y2, Z2), directdistance(xyz, X1, Y1, Z1, X2, Y2, Z2, D)},
% max distance from start point, this is necessary when a through point is identified the same as a start point.
FurthestOriginDistance = #max{D: category(IDF, CategoryFrom), assign(XF, YF, ZF, IDF, RxF, RyF, RzF),
    connectedthrough(Type, CategoryThrough, XF, YF, ZF, X1, Y1, Z1), connectedthrough(Type, CategoryThrough, XF, YF, ZF, X2, Y2, Z2),
     directdistance(xyz, XF, YF, ZF, X2, Y2, Z2, D)},
     connectivityrangenums(Distance), connectivityrangenums(FurthestOriginDistance),
     TotalDistance = Distance + FurthestOriginDistance,
TotalDistance < MinD.

distanceforassign(X1, Y1, Z1, Distance):-
requireddistance(Type, CategoryFrom, CategoryThrough, CategoryTo, MinD, MaxD), assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
category(ID1, CategoryFrom),
Distance = #max{D: category(ID2, CategoryTo), assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2),
  connectedthrough(Type, CategoryThrough, X1, Y1, Z1, X2, Y2, Z2), directdistance(xyz, X1, Y1, Z1, X2, Y2, Z2, D)}.

%tiledirections(Type, ID1, Ry, D) :-
%tile(ID1), tile(ID2),
%match(Type, D, ID1, _, 0, Ry, 0, 0, _,0), ryA(Ry).

%tiledirections(Type, ID1, Ry, D, ID2) :-
%tile(ID1), tile(ID2),
%match(Type, D, _, ID1, 0, _, 0, 0, Ry,0), ryA(Ry).

%:- metaposition(Direction), edgepositions(Direction, X1, Y1, Z1), cutoffside(Direction),
%currentblock(X1, Y1, Z1),  category(ID1, Category), cutoff(Type, Category),
% % category(ID2, void),
%not cutoffmatch(Type, Direction, X1,Y1,Z1).

%cutoffmatch(Type, Direction, X,Y,Z) :-
%% TODO put rule below back on because it is correct to not choose to move in the direction of the cutoff
%assign(X,Y,Z,ID, Rx,Ry,Rz),
%not match(Type, Direction, ID, _, Rx, Ry, Rz, 0, 0 ,0),
%match(strict, Direction, ID, void, Rx, Ry, Rz, 0 ,0 ,0),
%connectivitytype(Type).



%directconnectedoutwards(Type, ID1, Rx1, Ry1, Rz1, Direction) :-
%Rx1 = 0, Rz1 = 0, ryA(Ry1), connectivtytype(Type), tile(ID1), direction(Direction),
%tiledirections(Type, ID1, Ry1, Direction).






  %:- assign(X1, Y1, Z1, ID1, RX1, RY1, RZ1), all2connected(Type, Category),
  %category(ID1, Category),category(ID2, Category),
  %currentblock(X1, Y1, Z1), not 1 {assign(X2, Y2, Z2, ID2, RX2, RY2, RZ2):
  %  connected(Type, X1, Y1, Z1, X2, Y2, Z2), connected(Type, X2, Y2, Z2, X1, Y1, Z1)},
  %  not 1 {assign(X3, Y3, Z3, ID3, RX3, RY3, RZ3):
  %    connected(Type, X1, Y1, Z1, X3, Y3, Z3), connected(Type, X3, Y3, Z3, X1, Y1, Z1)}, adjacent(X2, Y2, Z2, X3, Y3, Z3),
  %   1 {assign(X2, Y2, Z2, ID2, RX2, RY2, RZ2):
  %    not connectedoutwards(Type, X2, Y2, Z2)}.



hardoverride.
% for every onlyoverride, only when override is defined for that cells
% it can have a tile with the override category.
:- category(ID, Category), onlyoverride(Category), hardoverride, currentblock(X,Y,Z),
1 {assign(X,Y,Z, ID, Rx, Ry, Rz): not override(X,Y,Z,Category)}.

% if override then the given cell must have a tile with that override category
:- tile(ID), category(ID, Category), hardoverride,
override(X,Y,Z, Category), currentblock(X,Y,Z),
not 1 {assign(X,Y,Z, ID, Rx, Ry, Rz): rxA(Rx), ryA(Ry), rzA(Rz)}.

% minimize all connected objectives to other blocks.
%allconnectedtootherblock(C) :- C = #count{X,Y,Z, Category, Type: assign(X,Y,Z,ID,Rx,Ry,Rz), category(ID, Category),  connectedoutwards(Type, X,Y,Z), cellboundary(X,Y,Z), allconnected(Type, Category),
%  not cellgoesoutside(X,Y,Z)}.
%  #minimize{C@4, X,Y,Z: currentblock(X,Y,Z), allconnectedtootherblock(C)}.


%:- not assign(0,0,1, wall, 0,1,0).
%:- not assign(1,0,0, window, 0,0,0).
%:- not assign(2,0,1, wall, 0,3,0).
%:- not assign(1,0,2, wall, 0,2,0).

#show assign/7.
