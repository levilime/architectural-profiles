%------------------------------------%
% shapeplacement LOGIC                        %

% Should replace the shape.lp logic.
% Places precomputed shapes.

% turn on with shapeplacementmode.

%----------------------------------- %

% can place a shape in the input space
%0 {shapeplacement((ShapeID, ShapeRot, P)):
%  shape(ShapeID),
%  rot(ShapeRot)
%  }  :-
%  cell(P).

% can place a shape in the input space, with any rotation
% only works for convex shapes, if concave shapes are allowed two shapes may shapecoverage
% the same origin position. Then multiple shapes are allowed at the same origin.
{shapeplacement((ShapeID, ShapeRot, P))} :-
  cell(P),rot(ShapeRot),shape(ShapeID),
  not limitshaperotation.

% cannot rotates shapes that are placed
% only turned on with rule limitshaperotation.
{shapeplacement((ShapeID, (0,0,0), P))} :-
  cell(P),rot(ShapeRot),shape(ShapeID),
  limitshaperotation.

shapename(Name) :-
  shapecontainer(Name, _).

% if there is an assign that means that there is a placedshapeposition
% at that position.
placedshapeposition(ShapeObj, P, ID, TileRot) :-
  cell(P),
  TileRot = (Rx, Ry, Rz),
  shapeplacement(ShapeObj),
  P = (X,Y,Z),
  validshapeposition(ShapeObj, P, ID, TileRot).

%1 {placedshapeposition(ShapeObj,  P, TileID, TileRot): shapeplacement(ShapeObj), tile(TileID), rot(TileRot)} 1 :-
%  cell(P), P = (X,Y,Z), currentblock(_, X,Y,Z), shapesolvingmode.

maxshapesize(S) :- S = (X,Y,Z),
  X =  #max{XC: shapedimensions(_, (XC, _, _))},
  Y =  #max{YC: shapedimensions(_, (_, YC, _))},
  Z =  #max{ZC: shapedimensions(_, (_, _, ZC))}.

shapecell((-X..X,-Y..Y,-Z..Z)) :- maxshapesize((X,Y,Z)).

% create shape positions of all shapes for all rotations, but these do not necessarily
% have start positions on or around origin (0,0,0)
misalignedrotatedshapeposition(ShapeDef, PN, TID, RTileRot) :-
  ShapeDef = (ShapeID, (Rx, Ry, Rz)),
  rxA(Rx),
  rzA(Rz),
  ryA(Ry),
  shapeposition(ShapeID, P, TID, TRy),
  rotateposition(P, Ry, PN),
  mod4(Ry + TRy, PR),
  RTileRot = (Rx, PR, Rz).

misalignedrotatedshapepositionorigin(ShapeDef, PO) :-
misalignedrotatedshapeposition(ShapeDef, _, _, _),
shapecell(PO),
PO = #min{(X,Y,Z):
  misalignedrotatedshapeposition(ShapeDef, (X, Y, Z), _, _)}.

% shape positions on which every has a point on xor around origin (0,0,0)
% this is created like this to make rotation be clockwise
rotatedshapeposition(ShapeDef, Prelative, TID, TRot) :-
  ShapeDef = (ShapeID, (Rx, 1, Rz)),
  rotatedshapepositioncounter((ShapeID, (Rx, 3, Rz)), Prelative, TID, TRot).
rotatedshapeposition(ShapeDef, Prelative, TID, TRot) :-
  ShapeDef = (ShapeID, (Rx, 0, Rz)),
  rotatedshapepositioncounter(ShapeDef, Prelative, TID, TRot).
rotatedshapeposition(ShapeDef, Prelative, TID, TRot) :-
  ShapeDef = (ShapeID, (Rx, 2, Rz)),
  rotatedshapepositioncounter(ShapeDef, Prelative, TID, TRot).
rotatedshapeposition(ShapeDef, Prelative, TID, TRot) :-
  ShapeDef = (ShapeID, (Rx, 3, Rz)),
  rotatedshapepositioncounter((ShapeID, (Rx, 1, Rz)), Prelative, TID, TRot).


rotatedshapepositioncounter(ShapeDef, Prelative, TID, TRot) :-
  misalignedrotatedshapeposition(ShapeDef, P, TID, TRot),
  misalignedrotatedshapepositionorigin(ShapeDef, PO),
  P =  (X0, Y0, Z0),
  PO = (X1, Y1, Z1),
  Prelative = (X0 - X1, Y0 - Y1, Z0 - Z1).

% rotate a position around the origin (0,0,0)
% rotates counterclockwise
rotateposition(P, RY, PN) :-
  P = (X, Y, Z),
  PN = (XN, YN, ZN),
  shapecell(P),
  shapecell(PN),
  cos(RY, A),
  sin(RY, B),
  XN = A * X + B * Z,
  YN = Y,
  ZN = - B * X + A * Z.

% the amount of cells covered by shapes
%shapecoverage(C) :- C =
%#count{Cell: Cell = (X,Y,Z),
%  cell(X,Y,Z),
%  placedshapeposition(_, Cell, _, _)
%  }.

% entrance match is an adjacency through an entrance adjacency.
entrancematch(Type, P1, P2) :-
  entrancetowards(Type, P1, P2),
  entrancetowards(Type, P2, P1).

% entrance exists from P1 to P2
entrancetowards(Type, P1, P2) :-
  P1 = (X1,Y1,Z1),
  P2 = (X2, Y2, Z2),
  directionmap(D, X1, Y1, Z1, X2, Y2, Z2),
  assign(X1, Y1, Z1, ID1, RX1, RY1, RZ1),
  %placedshapeposition(_, P, ID1, (RX1, RY1, RZ1))
  tileentrance(ID1, Type, D1),
  dir(D1, 0, RY1, 0, DN1),
  DN1 = D.

% a shape is closed if there is no shape position tile that moves with an
% relevant adjacency subtype outside of the shape
% ignores when the shape moves outside of the input
closed(ShapeObj, Type) :-
  shapeplacement(ShapeObj),
  alltypes(Type),
  %not shapetype(_, Type),
  not 1 {
    placedshapeposition(ShapeObj, P1, ID1, Rot1):
    ShapeObj = (SID, SRot, SP),
    directionmap(D, X1, Y1, Z1, X2, Y2, Z2),
    ST = Type,
    P1 = (X1, Y1, Z1),
    P2 = (X2, Y2, Z2),
    cell(P1),
    cell(P2),
    Rot1 = (Rx1, Ry1, Rz1),
    tiledirection(ST, ID1, Rot1, D),
    %tiledirections(Type, X1,Y1,Z1, ID1, Ry1, D),
    %match(ST, P1, P2),
    not entrancedirection(ST, ID1, Rot1, D),
    not placedshapeposition(ShapeObj, P2, _, _),
    not entrancetowards(Type, P2, P1)
  }.

tileswithininput(Type) :-
  closedontype(Type),
  not tilesoutsideinput(Type, _, _).

tilesoutsideinput(Type, ID, (X, Y, Z)) :-
  closedontype(Type),
  tile(ID),
  assign(X,Y,Z, ID, Rx, Ry, Rz),
  cellboundary(D, X, Y, Z),
  Rot = (Rx, Ry, Rz),
  tiledirection(Type, ID, Rot, D),
  not entrancedirection(Type, ID, Rot, D).

% add all other types to shapes that need to be checked
alltypes(Type) :-
  shapetype(_, Type).

% if there is a placedshapeposition that means there is an assign at that position.
% this method makes tile rotation of assignments free as long as the tiledirections
% and entrance directions are equal to that of the placedshapeposition tile rotation
1 {assign(X, Y, Z, ID, RxE, RyE, RzE):
  R = (Rx, Ry, Rz),
  equivalenttiledirectionrotation(ID, R, RE),
  equivalententrancedirectionrotation(ID, R, RE),
  RE = (RxE, RyE, RzE)
  %,R= RE
  } 1 :-
  placedshapeposition(ShapeObj, (X,Y,Z), ID, R),
  shapeplacement(ShapeObj),
  shapesolvingmode.

% if there is a placedshapeposition that means there is an assign at that position.
% this method is unused because it is necessary for shapes to exist together
% to somehow have tile rotations that give equivalent directions.
assign(X, Y, Z, ID, Rx, Ry, Rz) :-
  placedshapeposition(ShapeObj, (X,Y,Z), ID, R),
  shapeplacement(ShapeObj),
  R = (Rx, Ry, Rz),
  shapesolvingmode, false.

% two shapes may only connect with each other through an entrance
% if there exists a shapeadjacency for them
%illegaladjacentshapes(SID1,SID2, P1) :-
%  shapesolvingmode,
%  shapeplacement(ShapeObj1),
%  shapeplacement(ShapeObj2),
%  not ShapeObj1 = ShapeObj2,
%  ShapeObj1 = (SID1, SRot1, SP1),
%  ShapeObj2 = (SID2, SRot2, SP2),
%  placedshapeposition(ShapeObj1, P1, ID1, Rot1),
%  placedshapeposition(ShapeObj2, P2, ID2, Rot2),
%  adjacent(P1, P2),
%  shapetype(SID1, ST),
%  shapetype(SID2, ST),
%  entrancematch(ST, P1, P2),
%  not shapeadjacency(SID1, SID2, ST).
%#show illegaladjacentshapes/3.

%adjacentshapes(SID1,SID2, P1) :-
%  shapesolvingmode,
%  shapeplacement(ShapeObj1),
%  shapeplacement(ShapeObj2),
%  not ShapeObj1 = ShapeObj2,
%  ShapeObj1 = (SID1, SRot1, SP1),
%  ShapeObj2 = (SID2, SRot2, SP2),
%  placedshapeposition(ShapeObj1, P1, ID1, Rot1),
%  placedshapeposition(ShapeObj2, P2, ID2, Rot2),
%  adjacent(P1, P2).
%#show adjacentshapes/3.

%#show shapeplacement/1.

% two shapes may only connect with each other through an entrance
% if there exists a shapeadjacency for them
illegaladjacencyshape :-
  shapesolvingmode,
  1 {
    not shapeadjacency(SID1, SID2, ST):
    shapeplacement(ShapeObj1),
    shapeplacement(ShapeObj2),
    ShapeObj1 = (SID1, SRot1, SP1),
    ShapeObj2 = (SID2, SRot2, SP2),
    not ShapeObj1 = ShapeObj2,
    placedshapeposition(ShapeObj1, P1, ID1, Rot1),
    placedshapeposition(ShapeObj2, P2, ID2, Rot2),
    P1 = (X1, Y1, Z1),
    P2 = (X2, Y2, Z2),
    directionmap(D, X1, Y1, Z1, X2, Y2, Z2),
    tiledirection(ST, ID1, Rot1, D),
    oppositedirection(D, OD),
    tiledirection(ST, ID2, Rot2, OD),
    %shapetype(SID1, ST),
    %shapetype(SID2, ST)
    alltypes(ST)
    %not ST = air
  }.

illegaladjacencies(ID1, ID2, P1, D):- false,
  shapesolvingmode,
  not shapeadjacency(SID1, SID2, ST),
  shapeplacement(ShapeObj1),
  shapeplacement(ShapeObj2),
  ShapeObj1 = (SID1, SRot1, SP1),
  ShapeObj2 = (SID2, SRot2, SP2),
  not ShapeObj1 = ShapeObj2,
  placedshapeposition(ShapeObj1, P1, ID1, Rot1),
  placedshapeposition(ShapeObj2, P2, ID2, Rot2),
  cell(P1),
  P1 = (X1, Y1, Z1),
  P2 = (X2, Y2, Z2),
  Rot1 = (Rx1, Ry1, Rz1),
  Rot2 = (Rx2, Ry2, Rz2),
  direction(D),
  assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
  assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2),
  directionmap(D, X1, Y1, Z1, X2, Y2, Z2),
  tiledirection(ST, ID1, Rot1, D),
  oppositedirection(D, OD),
  tiledirection(ST, ID2, Rot2, OD),
  %shapetype(SID1, ST),
  %shapetype(SID2, ST)
  alltypes(ST).
% #show illegaladjacencies/3.

% TODO this has to be declarative from the profile and part of the template
%shapepulledbygravity(1).

% no floating shapes that can belong on the ground/ gravity
floatingshape(ShapeObj) :-
  shapeplacement(ShapeObj),
  ShapeObj = (SID, SRot, (SX, SY, SZ)),
  shapecontainer(Name, SID),
  shapepulledbygravity(Name),
  shapeadjacency(SID, ground, construction),
  not cellboundary(minusy, SX, SY, SZ),
  not 1 {
    placedshapeposition(ShapeObj, (X,Y,Z), ID, R):
    entrancedirection(construction, ID, R, minusy),
    directionmap(minusy, X, Y, Z, X2, Y2, Z2),
    assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2),
    not placedshapeposition(ShapeObj, (X2, Y2, Z2), _, _),
    tiledirection(construction, ID2, R, y)
    % tiledirections(construction, X2,Y2,Z2, _, _, y)
    %entrancetowards(construction, (X2, Y2, Z2), (X,Y,Z))
  }.

% process manyshapeadjacencies
shapeadjacency(SID1, SID2, ST) :-
  manyshapeadjacencies(ST, C1, C2),
  shapecategory(SID1, C1),
  shapecategory(SID2, C2).
  %shapetype(SID1, ST),
  %shapetype(SID2, ST).

% a shape adjacency is always defined bidirectional
shapeadjacency(SID1, SID2, ST) :-
  shapeadjacency(SID2, SID1, ST).
