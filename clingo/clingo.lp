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
%------------------------------------%
% Tile solving                       %

% turn on with tilesolvingmode.

%----------------------------------- %

% every cell needs to have an assignment
1 {assign(X,Y,Z,ID, RotX, RotY, RotZ): tile(ID), rxA(RotX), ryA(RotY), rzA(RotZ)} 1 :-
  cell(X,Y,Z), currentblock(_, X,Y,Z), tilesolvingmode.

% every cell can have an assignment
{assign(X,Y,Z,ID, RotX, RotY, RotZ): tile(ID), rxA(RotX), ryA(RotY), rzA(RotZ)} 1 :-
    cell(X,Y,Z), currentblock(_, X,Y,Z).

% no cell can ever have more than one assignment
% (this rule is only needed if the rule that there must be a tile in every cell
% is off)
:-
  cell(X,Y,Z), currentblock(_, X,Y,Z),
  2 {assign(X,Y,Z,ID, RotX, RotY, RotZ): tile(ID), rxA(RotX), ryA(RotY), rzA(RotZ)}.
%------------------------------------%
% purposefully connected shape LOGIC                   %

% Enforce that a shape that needs to be purposefully connected is that.
% Purposefully connected means that it connects by at least the Amount specified
% to other shapes.

%----------------------------------- %

:-
  purposefulshapeconnection(ShapeName, Type, Amount),
  shapecontainer(ShapeName, SID),
  shapeplacement(ShapeObj),
  ShapeObj = (SID, _, _),
  placedshapeposition(ShapeObj, (X,Y,Z), ID, Rot),
  not Amount {
    assign(X2,Y2,Z2, ID2, Rx2, Ry2, Rz2):
      tiledirection(Type, ID, Rot, D),
      directionmap(D, X, Y, Z, X2, Y2, Z2),
      Rot2 = (Rx2, Ry2, Rz2),
      oppositedirection(D, DR),
      tiledirection(Type, ID2, Rot2, DR)
  }.
%------------------------------------%
% Shape solving                       %

% turn on with shapesolvingmode.

%----------------------------------- %

% if there exists a shape then put shapesolvingmode on.
shapesolvingmode :- shape(_), not shapegeneratormode.

% a placedshapeposition can be placed if there is an accomponying shapeplacement
% TODO delete because it is replaced by an other rule
%1 {placedshapeposition(ShapeObj, P, ID, TileRot):
%  validshapeposition(ShapeObj, P, ID, TileRot),
%  shapeplacement(ShapeObj)
%  } 1 :-
%  cell(P), P = (X,Y,Z), currentblock(_, X,Y,Z),
%  shapesolvingmode, false.

% when a shape is placed, than this entails that the tiles that make up this
% shape are to be placed in the cells
validshapeposition(ShapeObj,  P, TileID, TileRot) :-
  ShapeObj = (ShapeID, ShapeRot, OP),
  shapeplacement(ShapeObj),
  rotatedshapeposition((ShapeID, ShapeRot), SP, TileID, TileRot),
  P = (X1, Y1, Z1), OP = (X0, Y0, Z0),
  SP = (X1 - X0, Y1 - Y0, Z1 - Z0), cell(P).
  %shapeplacement(ShapeObj1),
  %not validshapeposition(ShapeObj1, P, _, _),
  %ShapeObj != ShapeObj1.

%1 {validshapeposition(ShapeObj,  P, TileID, TileRot): shapeplacement(ShapeObj), tile(TileID), rot(TileRot)} 1 :-
%  cell(P), P = (X,Y,Z), currentblock(_, X,Y,Z), shapesolvingmode.

%:-
%  shapesolvingmode,
%  not 1 {validshapeposition(ShapeObj,  P, TileID, TileRot):
%     cell(P)} 1.

% TODO delete, rule below is probably not necessary because validshapeposition
% can only be created through a shapeplacement, that in the end needs to
% result in tiles being placed and overlap is not possible
:-
  shapesolvingmode,
  validshapeposition(ShapeObj1, P, _, _),
  validshapeposition(ShapeObj2, P, _, _),
  ShapeObj1 != ShapeObj2.

:-
  shapesolvingmode,
  cell(P),
  not {validshapeposition(_, P, _, _)} 1.

% every cell must be covered by a shape
:-
  cell(P),
  not placedshapeposition(_, P, _, _),
  shapesolvingmode.

%uniqueplaced(S) :-
%  S = #count{P : cell(P), placedshapeposition(ShapeObj, P, _, _), ShapeObj = (SID,_,_),
%     not SID = void}.

%#maximize{ W@3, P:
%  cell(P), placedshapeposition(ShapeObj, P, _, _), ShapeObj = (SID,_,_),
%     not SID = void,
%  validshapeposition(ShapeObj, P, _, _),
%  shapeplacement(ShapeObj), uniqueplaced(W) }.

%#show uniqueplaced/1.

% if there is room to place a tile accomponying a shape
% at a certain position than it should be placed.
notileplacementforplacedshape(ShapeObj, P, ID, TileRot) :-
  shapeplacement(ShapeObj),
  validshapeposition(ShapeObj, P, ID, TileRot),
  cell(P),
  not placedshapeposition(ShapeObj, P, ID, TileRot).

% this should work without any additional logic so can be turned off
% TODO delete
:- notileplacementforplacedshape(_,_,_,_), shapesolvingmode, false.

% there may not be shapes adjacent that are not allowed to be adjacent
:- illegaladjacencyshape, shapesolvingmode.

% no cell can ever have more than one assignment
% (this rule is only needed if the rule above is off)
%:-
%  not shapesolvingmode,
%  cell(X,Y,Z), currentblock(_, X,Y,Z),
%  2 {placedshapeposition(_, (X,Y,Z), ID, (RotX, RotY, RotZ)):
%    validshapeposition(ShapeObj, P, ID, TileRot),
%    shapeplacement(ShapeObj),
%    TileRot = (RotX, RotY, RotZ),
%    tile(ID), rxA(RotX), ryA(RotY), rzA(RotZ)}.

% all shapes must be closed additionaly in the adjacency types that are not part
% of the shape creation.
:-
  shapesolvingmode,
  1 {
    shapeplacement(ShapeObj):
    ShapeObj = (SID, _, _),
    alltypes(Type),
    not shapetype(SID, Type),
    not closed(ShapeObj, Type)
  }.

% FIXME hardcoded here that some types may not go outside
%closedontype(routing) :- shapesolvingmode.
%closedontype(construction) :- shapesolvingmode.
%:- not tileswithininput(routing), shapesolvingmode.
%:- not tileswithininput(construction), shapesolvingmode.

% test rule to see how it scales
%:- 10 {shapeplacement((SID, _, _)): SID = 1, shape(SID)}, shapesolvingmode.

% add ground, only shapes that have a shapeadjacency with the ground
% can be put on the ground
:-
  shape(SID),
  placedshapeposition((SID, _, _), (X,Y,Z), _, _),
  cellboundary(minusy, X, Y, Z),
  not shapeadjacency(ground, SID, construction), shapesolvingmode.

%shapeadjacency(SID, ground, construction) :-
%  shapeadjacency(ground, SID, construction), shape(SID).
%shapeadjacency(ground, SID, construction) :-
%  shapeadjacency(SID, ground, construction), shape(SID).

% floating shapes that can belong on the ground/ gravity
:- floatingshape(ShapeObj), shapesolvingmode.
%------------------------------------%
% shapegenerator LOGIC                        %

% turn on with shapegeneratormode.

% turn off that all cells need an assignment, only one shape needs to exist
% that spans the input space

%----------------------------------- %

shapegeneratormode :- requiredshape(_).

cutoffside(x) :- shapegeneratormode.
cutoffside(z) :- shapegeneratormode.
cutoffside(minusx) :- shapegeneratormode.
cutoffside(minusz) :- shapegeneratormode.

% if requiredshape is defined than that shape must exist in the solution
1 {shapeplacement(ShapeObj): cell(X,Y,Z), ShapeObj = (ShapeID, Rot, (X,Y,Z))} 1 :-
  requiredshape(ShapeDef),
  ShapeDef = (ShapeID, Rot).


% if there is an assign that means that there is a placedshapeposition
% at that position.
placedshapeposition(ShapeObj, (X,Y,Z), ID, (Rx, Ry, Rz)) :-
  shapegeneratormode,
  assign(X, Y, Z, ID, Rx, Ry, Rz),
  shapeplacement(ShapeObj).

% if multipleshapegeneratormode is on, than the shape defined in ShapeDef
% may exist multiple times.


% a shape in shapegeneratormode must touch all edges of the input space
:-
    shapegeneratormode,
    direction(D),
    cellboundary(D, X,Y,Z),
    P=(X,Y,Z),
    shapeplacement(ShapeObj),
    not placedshapeposition(ShapeObj, P, _, _).

% in shapegenerator mode we are only interested in the shape created at the origin
:-
  shapegeneratormode,
  shapeplacement((_, Rot, P)),
  not P = (0,0,0).

% in shape generator mode we are only interested in a shape that is not rotated,
% as it can be rotated after the initial generation
:-
  shapegeneratormode,
  shapeplacement((_, Rot, P)),
  not Rot = (0,0,0).

% tiles that are placed need to match the shape that is being created
:- shapegeneratormode,
  placedshapeposition(ShapeObj, (X,Y,Z), ID, _),
  ShapeObj = (ShapeID, _, _),
  shapecategory(ShapeID, Category),
  not category(ID, Category).

validshapeposition(ShapeObj, P, ID, TileRot) :-
  shapegeneratormode,
  placedshapeposition(ShapeObj, P, ID, TileRot).


% there has to be at least one entrance
% the entrance must be on the cellboundary, to force that it can be reached block_from_result
% the outside
:- shapegeneratormode,
  shapeplacement(ShapeObj),
  ShapeObj = (ShapeID, _, _),
  shapetype(ShapeID, Type),
  not 1 {placedshapeposition(ShapeObj, (X,Y,Z), ID, Rot):
    entrancedirection(Type, ID, Rot, D), cellboundary(D, X, Y, Z)
    }.

% if shape entrance is specified, than that amount of entrances must exist
:- shapegeneratormode,
  shapeplacement(ShapeObj),
  ShapeObj = (ShapeID, _, _),
  shapetype(ShapeID, Type),
  shapeentrance(ShapeID, MinEntrances, MaxEntrances),
  not MinEntrances {placedshapeposition(ShapeObj, (X,Y,Z), ID, Rot):
    entrancedirection(Type, ID, Rot, D), cellboundary(D, X, Y, Z)} MaxEntrances.

% if entrances at level are specified for shape, then entarnces may only exist on those levels
:- shapegeneratormode,
  shapeplacement(ShapeObj),
  ShapeObj = (ShapeID, _, _),
  shapetype(ShapeID, Type),
  shapeentranceatheightlevel(ShapeID, _),
  1 {placedshapeposition(ShapeObj, (X,Y,Z), ID, Rot):
    cellboundary(D, X,Y,Z),
    not shapeentranceatheightlevel(ShapeID, Y),
    entrancedirection(Type, ID, Rot, D)}.

% shape must be closed within the input size
:-
  shapegeneratormode,
  shapeplacement(ShapeObj),
  ShapeObj = (SID, _, _),
  placedshapeposition(ShapeObj, (X,Y,Z), ID, Rot),
  shapetype(SID, Type),
  Rot = (Rx, Ry, Rz),
  %tiledirections(Type, X,Y,Z, ID, Ry, D),
  tiledirection(Type, ID, Rot, D),
  cellboundary(D, X,Y,Z),
  % exempt entrances, they count as closed
  not entrancedirection(Type, ID, Rot, D).

% the shape created in shapegeneratormode must be closed
:-
  shapegeneratormode,
  requiredshape(ShapeDef),
  ShapeDef = (ShapeID, Rot),
  ShapeObj = (ShapeID, Rot, P),
  shapeplacement(ShapeObj),
  shapetype(ShapeID, Type),
  not closed(ShapeObj, Type).

% in shapegeneratormode all adjacency subsets of the primary type must be answered
% NOT CORRECT! (because this does not have to be the case
% (e.g. stairs in room does not connect to all adjacent cells))
%:-
%  shapegeneratormode, false,
%  shapeplacement(ShapeObj),
%  ShapeObj = (SID, _, _),
%  placedshapeposition(ShapeObj, (X,Y,Z), ID, Rot),
%  shapetype(SID, Type),
%  tiledirection(Type, ID, Rot, D),
%  not entrancedirection(Type, ID, Rot, D),
%  directionmap(D, X, Y, Z, X2, Y2, Z2),
%  placedshapeposition(ShapeObj, (X2,Y2,Z2), ID2, Rot2),
%  oppositedirection(D, OD),
%  tiledirection(Type, ID2, Rot2, OD).
% a few concepts are essential to understand the code.
% - cell: a container in which a tile must be placed
% - currentblock: denotes the cells that needs to be assigned this solving step
% - Type: denotes adjacency subtype, a subset of the strict adjacencies such as traversal
% - connectedness: whether there is a path from one cell to another cell given a certain
% adjacency subtype.
% - shape: a collection of cell assignments that form a group with a semantic meaning, such as a room, or a building
% an adjacency subtype.

% This code is auto generated and contains all logic the system may need.
% logic is enabled by adding appropriate rules that activate them inserted by the
% overarching solver.

% there are a number of modes the solver can be in, top constraints that largely
% control what happens, these are turned on or off by stating the following rules.

% tilesolvingmode.
% tile solving mode means for every cell there must be a tile assignment.

% wangtileblocksmode.
% wang tile block mode means that there are blocks that should be equal.

% shapegeneratormode.
% mode to generate a shape.

% shapeplacementmode.
% can only add tiles by adding shapes, and the shapes must satisfy the
% shape adjacencies.
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
%------------------------------------%
% Global connected LOGIC                   %

% here called simpleconnected, this controls,
% global connectivity constraints such as:
% every traversable tile must be reachable from anywhere

%----------------------------------- %

originatingconnectiontile(Type, MinX, MinY, MinZ) :-
 simpleallconnected(Type),
 MinX = #min{X: typedtile(X,Y,Z, Type) },
 MinY = #min{Y: typedtile(X,Y,Z, Type) },
 MinZ = #min{Z: typedtile(X,Y,Z, Type) }.

% sanity checkwhether there is only one originatingconnectiontile per simpleallconnected
%:- 2 { originatingconnectiontile(Type, Category, X, Y, Z)}, simpleallconnected(Type, Category).
%assignedcategories(X,Y,Z, Category) :-
%  assign(X,Y,Z, ID, Rx1, Ry1, Rz1),
%  category(ID, Category),
%  simpleallconnected(Type, Category),
%  currentblock(_, X,Y,Z).

typedtile(X,Y,Z, Type) :-
  assign(X,Y,Z, ID, Rx1, Ry1, Rz1),
  simpleallconnected(Type),
  currentblock(_, X,Y,Z),
  1 {tiledirection(Type, ID, _, _)}.

originconnected(Type, X1, Y1, Z1) :-
  simpleallconnected(Type),
  equalposition(X1, Y1, Z1, X2, Y2, Z2),
  originatingconnectiontile(Type, X2, Y2, Z2).
% transative
originconnected(Type, X1, Y1, Z1) :-
  simpleallconnected(Type),
  assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
  directionmap(Dir, X1, Y1, Z1, X2, Y2, Z2),
  %tiledirection(Type, ID1, (Rx1, Ry1, Rz1), Dir), oppositedirection(Dir, ODir),
  %tiledirection(Type, ID2, (Rx2, Ry2, Rz2), ODir),
  match(Type, Dir, ID1, ID2, Rx1, Ry1, Rz1, Rx2, Ry2, Rz2),
  assign(X2, Y2, Z2, ID2, Rx2, Ry2, Rz2), originconnected(Type, X2, Y2, Z2).

connectivitytype(Type) :- simpleallconnected(Type, _).

simpleallconnected(Type) :- simpleallconnected(Type, _).

failedconnected(X1, Y1, Z1, ID1) :-
  simpleallconnected(Type),
  assign(X1, Y1, Z1, ID1, Rx1, Ry1, Rz1),
  currentblock(_, X1, Y1, Z1),
  %category(ID1, Category),
  typedtile(X1,Y1,Z1, Type),
  not originconnected(Type, X1, Y1, Z1)
  % currently connectedoutwards is turned off!
  %,not connectedoutwards(Type, X1, Y1, Z1)
.

% there may not be a traversable tile that should be traversable but is not
%@toggle
:- failedconnected(X1, Y1, Z1, ID1).

%#show failedconnected/4.
%#show connectedoutwards/4.

% #show originatingconnectiontile/5.
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
% whether a shape is closed within the input,
% used in finding non atomic shapes.
:- closedontype(Type), not tileswithininput(Type).

hasshape(Name) :- requiredshapeid(Name), 1 {shapeplacement((SID, _, _)): shapecontainer(Name, SID)}.
:- requiredshapeid(Name), not hasshape(Name).
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

hasshapegeneral(Name) :- shapecontainer(Name, SID), 1 {placedshapeposition((SID, _, _), _, _, _)}.
%:- not 1 {hasshapegeneral(_)}, shapesolvingmode.
% all shape represented is ignored if there is a shapeoccurence requirement
:- shapecontainer(Name, _), not hasshapegeneral(Name), shapesolvingmode,
  not shapeoccurence(_,_,_).
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
#show assign/7.

cellamount(A) :- A = #count{X: cell(X)}.
#show cellamount/1.
%#show uniquetiles/1.
%#show densityscore/1.

% TEMPLATE LOGIC BELOW



cell(0..2,0..2,0..2). 
currentblock(0,0..2,0..2,0..2).

%tile(ID).
%category(ID, CATEGORY).
tile(void).
category(void,void).
tile(flatsurface).
category(flatsurface,routing).
category(flatsurface,exterior).
category(flatsurface,built).
tile(stairs).
category(stairs,routing).
category(stairs,exterior).
category(stairs,interior).
category(stairs,built).
category(stairs,elevate).
tile(void_above_stairs).
category(void_above_stairs,exterior).
category(void_above_stairs,built).
category(void_above_stairs,interior).
category(void_above_stairs,routing).
tile(corner).
category(corner,interior).
category(corner,routing).
category(corner,built).
tile(wall).
category(wall,interior).
category(wall,routing).
category(wall,wall).
category(wall,built).
tile(door).
category(door,interior).
category(door,routing).
category(door,door).
category(door,built).
tile(window).
category(window,interior).
category(window,routing).
category(window,window).
category(window,built).
tile(inside).
category(inside,interior).
category(inside,routing).
category(inside,built).
tile(roof).
category(roof,roof).
category(roof,built).

%tile entrances
tileentrance(flatsurface, routing, x).
tileentrance(flatsurface, routing, minusx).
tileentrance(flatsurface, routing, z).
tileentrance(flatsurface, routing, minusz).
tileentrance(flatsurface, construction, minusy).
tileentrance(stairs, routing, minusz).
tileentrance(stairs, construction, minusy).
tileentrance(void_above_stairs, routing, z).
tileentrance(corner, construction, minusy).
tileentrance(wall, construction, minusy).
tileentrance(door, routing, minusz).
tileentrance(door, construction, minusy).
tileentrance(window, construction, minusy).
tileentrance(inside, construction, minusy).
tileentrance(roof, construction, minusy).

%tile entrances
tiledirection(flatsurface, routing, x).
tiledirection(flatsurface, routing, minusx).
tiledirection(flatsurface, routing, z).
tiledirection(flatsurface, routing, minusz).
tiledirection(stairs, routing, minusz).
tiledirection(stairs, routing, y).
tiledirection(stairs, construction, minusy).
tiledirection(stairs, construction, y).
tiledirection(void_above_stairs, routing, minusy).
tiledirection(void_above_stairs, routing, z).
tiledirection(void_above_stairs, construction, minusy).
tiledirection(corner, routing, z).
tiledirection(corner, routing, x).
tiledirection(corner, construction, x).
tiledirection(corner, construction, z).
tiledirection(corner, construction, y).
tiledirection(wall, routing, minusx).
tiledirection(wall, routing, x).
tiledirection(wall, routing, z).
tiledirection(wall, construction, x).
tiledirection(wall, construction, minusx).
tiledirection(wall, construction, z).
tiledirection(wall, construction, y).
tiledirection(door, routing, x).
tiledirection(door, routing, minusx).
tiledirection(door, routing, z).
tiledirection(door, routing, minusz).
tiledirection(door, construction, x).
tiledirection(door, construction, minusx).
tiledirection(door, construction, z).
tiledirection(door, construction, y).
tiledirection(window, routing, minusx).
tiledirection(window, routing, x).
tiledirection(window, routing, z).
tiledirection(window, construction, x).
tiledirection(window, construction, minusx).
tiledirection(window, construction, z).
tiledirection(window, construction, y).
tiledirection(inside, routing, x).
tiledirection(inside, routing, minusx).
tiledirection(inside, routing, z).
tiledirection(inside, routing, minusz).
tiledirection(inside, construction, y).
tiledirection(inside, construction, x).
tiledirection(inside, construction, z).
tiledirection(inside, construction, minusz).
tiledirection(inside, construction, minusx).
tiledirection(roof, construction, minusy).

%adjacencies for Type: strict.
%adjacency(Type, ID1, ID2, D, Rx, Ry, Rz).
adjacency(strict,void,void,x,0,0,0).
adjacency(strict,void,roof,x,0,0,0).
adjacency(strict,void,corner,x,0,0,0).
adjacency(strict,void,wall,x,0,1,0).
adjacency(strict,void,window,x,0,1,0).
adjacency(strict,void,corner,x,0,1,0).
adjacency(strict,void,void_above_stairs,x,0,1,0).
adjacency(strict,void,stairs,x,0,0,0).
adjacency(strict,void,flatsurface,x,0,0,0).
adjacency(strict,void,void_above_stairs,x,0,0,0).
adjacency(strict,void,void_above_stairs,x,0,2,0).
adjacency(strict,void,stairs,x,0,3,0).
adjacency(strict,void,stairs,x,0,2,0).
adjacency(strict,void,void,minusx,0,0,0).
adjacency(strict,void,roof,minusx,0,0,0).
adjacency(strict,void,corner,minusx,0,3,0).
adjacency(strict,void,corner,minusx,0,2,0).
adjacency(strict,void,window,minusx,0,3,0).
adjacency(strict,void,void_above_stairs,minusx,0,3,0).
adjacency(strict,void,flatsurface,minusx,0,0,0).
adjacency(strict,void,void_above_stairs,minusx,0,0,0).
adjacency(strict,void,void_above_stairs,minusx,0,2,0).
adjacency(strict,void,stairs,minusx,0,1,0).
adjacency(strict,void,wall,minusx,0,3,0).
adjacency(strict,void,stairs,minusx,0,0,0).
adjacency(strict,void,void,y,0,0,0).
adjacency(strict,void,corner,y,0,3,0).
adjacency(strict,void,flatsurface,y,0,0,0).
adjacency(strict,void,wall,y,0,2,0).
adjacency(strict,void,stairs,y,0,2,0).
adjacency(strict,void,stairs,y,0,1,0).
adjacency(strict,void,door,y,0,0,0).
adjacency(strict,void,stairs,y,0,3,0).
adjacency(strict,void,corner,y,0,0,0).
adjacency(strict,void,window,y,0,1,0).
adjacency(strict,void,door,y,0,1,0).
adjacency(strict,void,wall,y,0,3,0).
adjacency(strict,void,corner,y,0,1,0).
adjacency(strict,void,corner,y,0,2,0).
adjacency(strict,void,window,y,0,3,0).
adjacency(strict,void,wall,y,0,1,0).
adjacency(strict,void,stairs,y,0,0,0).
adjacency(strict,void,void,minusy,0,0,0).
adjacency(strict,void,flatsurface,minusy,0,0,0).
adjacency(strict,void,void_above_stairs,minusy,0,1,0).
adjacency(strict,void,void_above_stairs,minusy,0,3,0).
adjacency(strict,void,void_above_stairs,minusy,0,2,0).
adjacency(strict,void,void_above_stairs,minusy,0,0,0).
adjacency(strict,void,roof,minusy,0,0,0).
adjacency(strict,void,void,z,0,0,0).
adjacency(strict,void,roof,z,0,0,0).
adjacency(strict,void,corner,z,0,3,0).
adjacency(strict,void,corner,z,0,0,0).
adjacency(strict,void,void_above_stairs,z,0,0,0).
adjacency(strict,void,void_above_stairs,z,0,3,0).
adjacency(strict,void,flatsurface,z,0,0,0).
adjacency(strict,void,void_above_stairs,z,0,1,0).
adjacency(strict,void,stairs,z,0,2,0).
adjacency(strict,void,wall,z,0,0,0).
adjacency(strict,void,stairs,z,0,3,0).
adjacency(strict,void,window,z,0,0,0).
adjacency(strict,void,stairs,z,0,1,0).
adjacency(strict,void,void,minusz,0,0,0).
adjacency(strict,void,roof,minusz,0,0,0).
adjacency(strict,void,corner,minusz,0,1,0).
adjacency(strict,void,corner,minusz,0,2,0).
adjacency(strict,void,window,minusz,0,2,0).
adjacency(strict,void,wall,minusz,0,2,0).
adjacency(strict,void,flatsurface,minusz,0,0,0).
adjacency(strict,void,void_above_stairs,minusz,0,1,0).
adjacency(strict,void,void_above_stairs,minusz,0,3,0).
adjacency(strict,void,stairs,minusz,0,0,0).
adjacency(strict,void,stairs,minusz,0,3,0).
adjacency(strict,void,void_above_stairs,minusz,0,2,0).
adjacency(strict,flatsurface,flatsurface,x,0,0,0).
adjacency(strict,flatsurface,corner,x,0,0,0).
adjacency(strict,flatsurface,door,x,0,1,0).
adjacency(strict,flatsurface,corner,x,0,1,0).
adjacency(strict,flatsurface,window,x,0,1,0).
adjacency(strict,flatsurface,wall,x,0,1,0).
adjacency(strict,flatsurface,stairs,x,0,3,0).
adjacency(strict,flatsurface,stairs,x,0,1,0).
adjacency(strict,flatsurface,stairs,x,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,x,0,3,0).
adjacency(strict,flatsurface,void_above_stairs,x,0,1,0).
adjacency(strict,flatsurface,void,x,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,x,0,0,0).
adjacency(strict,flatsurface,stairs,x,0,2,0).
adjacency(strict,flatsurface,roof,x,0,0,0).
adjacency(strict,flatsurface,void,y,0,0,0).
adjacency(strict,flatsurface,wall,y,0,2,0).
adjacency(strict,flatsurface,door,y,0,2,0).
adjacency(strict,flatsurface,flatsurface,y,0,0,0).
adjacency(strict,flatsurface,corner,y,0,0,0).
adjacency(strict,flatsurface,window,y,0,0,0).
adjacency(strict,flatsurface,corner,y,0,3,0).
adjacency(strict,flatsurface,window,y,0,1,0).
adjacency(strict,flatsurface,door,y,0,1,0).
adjacency(strict,flatsurface,door,y,0,0,0).
adjacency(strict,flatsurface,stairs,y,0,1,0).
adjacency(strict,flatsurface,corner,y,0,1,0).
adjacency(strict,flatsurface,corner,y,0,2,0).
adjacency(strict,flatsurface,stairs,y,0,0,0).
adjacency(strict,flatsurface,stairs,y,0,3,0).
adjacency(strict,flatsurface,stairs,y,0,2,0).
adjacency(strict,flatsurface,wall,y,0,1,0).
adjacency(strict,flatsurface,door,y,0,3,0).
adjacency(strict,flatsurface,wall,y,0,0,0).
adjacency(strict,flatsurface,wall,y,0,3,0).
adjacency(strict,flatsurface,window,y,0,3,0).
adjacency(strict,flatsurface,flatsurface,z,0,0,0).
adjacency(strict,flatsurface,corner,z,0,0,0).
adjacency(strict,flatsurface,corner,z,0,3,0).
adjacency(strict,flatsurface,wall,z,0,0,0).
adjacency(strict,flatsurface,door,z,0,0,0).
adjacency(strict,flatsurface,window,z,0,0,0).
adjacency(strict,flatsurface,stairs,z,0,2,0).
adjacency(strict,flatsurface,stairs,z,0,1,0).
adjacency(strict,flatsurface,void,z,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,z,0,1,0).
adjacency(strict,flatsurface,stairs,z,0,0,0).
adjacency(strict,flatsurface,stairs,z,0,3,0).
adjacency(strict,flatsurface,void_above_stairs,z,0,3,0).
adjacency(strict,flatsurface,void_above_stairs,z,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,z,0,2,0).
adjacency(strict,flatsurface,roof,z,0,0,0).
adjacency(strict,flatsurface,flatsurface,minusx,0,0,0).
adjacency(strict,flatsurface,corner,minusx,0,3,0).
adjacency(strict,flatsurface,wall,minusx,0,3,0).
adjacency(strict,flatsurface,corner,minusx,0,2,0).
adjacency(strict,flatsurface,door,minusx,0,3,0).
adjacency(strict,flatsurface,window,minusx,0,3,0).
adjacency(strict,flatsurface,stairs,minusx,0,3,0).
adjacency(strict,flatsurface,void_above_stairs,minusx,0,1,0).
adjacency(strict,flatsurface,stairs,minusx,0,1,0).
adjacency(strict,flatsurface,stairs,minusx,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,minusx,0,3,0).
adjacency(strict,flatsurface,void,minusx,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,minusx,0,0,0).
adjacency(strict,flatsurface,stairs,minusx,0,2,0).
adjacency(strict,flatsurface,void_above_stairs,minusx,0,2,0).
adjacency(strict,flatsurface,roof,minusx,0,0,0).
adjacency(strict,flatsurface,flatsurface,minusz,0,0,0).
adjacency(strict,flatsurface,corner,minusz,0,1,0).
adjacency(strict,flatsurface,corner,minusz,0,2,0).
adjacency(strict,flatsurface,wall,minusz,0,2,0).
adjacency(strict,flatsurface,door,minusz,0,2,0).
adjacency(strict,flatsurface,window,minusz,0,2,0).
adjacency(strict,flatsurface,stairs,minusz,0,2,0).
adjacency(strict,flatsurface,stairs,minusz,0,1,0).
adjacency(strict,flatsurface,void_above_stairs,minusz,0,0,0).
adjacency(strict,flatsurface,stairs,minusz,0,3,0).
adjacency(strict,flatsurface,void,minusz,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,minusz,0,3,0).
adjacency(strict,flatsurface,stairs,minusz,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,minusz,0,1,0).
adjacency(strict,flatsurface,door,minusy,0,2,0).
adjacency(strict,flatsurface,flatsurface,minusy,0,0,0).
adjacency(strict,flatsurface,corner,minusy,0,1,0).
adjacency(strict,flatsurface,wall,minusy,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,minusy,0,1,0).
adjacency(strict,flatsurface,wall,minusy,0,2,0).
adjacency(strict,flatsurface,corner,minusy,0,0,0).
adjacency(strict,flatsurface,corner,minusy,0,2,0).
adjacency(strict,flatsurface,door,minusy,0,0,0).
adjacency(strict,flatsurface,window,minusy,0,1,0).
adjacency(strict,flatsurface,inside,minusy,0,0,0).
adjacency(strict,flatsurface,void,minusy,0,0,0).
adjacency(strict,flatsurface,void_above_stairs,minusy,0,0,0).
adjacency(strict,flatsurface,door,minusy,0,3,0).
adjacency(strict,flatsurface,corner,minusy,0,3,0).
adjacency(strict,flatsurface,window,minusy,0,0,0).
adjacency(strict,flatsurface,wall,minusy,0,1,0).
adjacency(strict,flatsurface,wall,minusy,0,3,0).
adjacency(strict,flatsurface,door,minusy,0,1,0).
adjacency(strict,flatsurface,window,minusy,0,2,0).
adjacency(strict,flatsurface,window,minusy,0,3,0).
adjacency(strict,flatsurface,void_above_stairs,minusy,0,2,0).
adjacency(strict,roof,roof,x,0,0,0).
adjacency(strict,roof,void,x,0,0,0).
adjacency(strict,roof,flatsurface,x,0,0,0).
adjacency(strict,roof,void,minusx,0,0,0).
adjacency(strict,roof,roof,minusx,0,0,0).
adjacency(strict,roof,flatsurface,minusx,0,0,0).
adjacency(strict,roof,corner,minusy,0,0,0).
adjacency(strict,roof,corner,minusy,0,3,0).
adjacency(strict,roof,door,minusy,0,1,0).
adjacency(strict,roof,wall,minusy,0,3,0).
adjacency(strict,roof,corner,minusy,0,1,0).
adjacency(strict,roof,corner,minusy,0,2,0).
adjacency(strict,roof,wall,minusy,0,0,0).
adjacency(strict,roof,inside,minusy,0,0,0).
adjacency(strict,roof,wall,minusy,0,2,0).
adjacency(strict,roof,window,minusy,0,3,0).
adjacency(strict,roof,door,minusy,0,0,0).
adjacency(strict,roof,window,minusy,0,1,0).
adjacency(strict,roof,door,minusy,0,3,0).
adjacency(strict,roof,window,minusy,0,2,0).
adjacency(strict,roof,door,minusy,0,2,0).
adjacency(strict,roof,window,minusy,0,0,0).
adjacency(strict,roof,wall,minusy,0,1,0).
adjacency(strict,roof,roof,z,0,0,0).
adjacency(strict,roof,void,z,0,0,0).
adjacency(strict,roof,void,minusz,0,0,0).
adjacency(strict,roof,roof,minusz,0,0,0).
adjacency(strict,roof,flatsurface,minusz,0,0,0).
adjacency(strict,roof,void,y,0,0,0).
adjacency(strict,corner,corner,x,0,3,0).
adjacency(strict,corner,wall,x,0,0,0).
adjacency(strict,corner,door,x,0,0,0).
adjacency(strict,corner,window,x,0,0,0).
adjacency(strict,corner,flatsurface,minusx,0,0,0).
adjacency(strict,corner,flatsurface,minusx,0,1,0).
adjacency(strict,corner,flatsurface,minusx,0,3,0).
adjacency(strict,corner,flatsurface,minusx,0,2,0).
adjacency(strict,corner,corner,minusx,0,3,0).
adjacency(strict,corner,corner,minusx,0,2,0).
adjacency(strict,corner,void,minusx,0,3,0).
adjacency(strict,corner,void,minusx,0,0,0).
adjacency(strict,corner,stairs,minusx,0,0,0).
adjacency(strict,corner,void,minusx,0,1,0).
adjacency(strict,corner,void,minusx,0,2,0).
adjacency(strict,corner,void_above_stairs,minusx,0,0,0).
adjacency(strict,corner,stairs,minusx,0,1,0).
adjacency(strict,corner,void_above_stairs,minusx,0,2,0).
adjacency(strict,corner,void_above_stairs,minusx,0,3,0).
adjacency(strict,corner,roof,y,0,0,0).
adjacency(strict,corner,roof,y,0,1,0).
adjacency(strict,corner,roof,y,0,3,0).
adjacency(strict,corner,roof,y,0,2,0).
adjacency(strict,corner,corner,y,0,3,0).
adjacency(strict,corner,wall,y,0,1,0).
adjacency(strict,corner,corner,y,0,0,0).
adjacency(strict,corner,flatsurface,y,0,3,0).
adjacency(strict,corner,corner,y,0,2,0).
adjacency(strict,corner,wall,y,0,0,0).
adjacency(strict,corner,door,y,0,2,0).
adjacency(strict,corner,corner,y,0,1,0).
adjacency(strict,corner,stairs,y,0,1,0).
adjacency(strict,corner,door,y,0,3,0).
adjacency(strict,corner,flatsurface,y,0,0,0).
adjacency(strict,corner,door,y,0,1,0).
adjacency(strict,corner,flatsurface,y,0,2,0).
adjacency(strict,corner,flatsurface,y,0,1,0).
adjacency(strict,corner,door,y,0,0,0).
adjacency(strict,corner,window,y,0,1,0).
adjacency(strict,corner,stairs,y,0,0,0).
adjacency(strict,corner,window,y,0,0,0).
adjacency(strict,corner,stairs,y,0,3,0).
adjacency(strict,corner,door,z,0,1,0).
adjacency(strict,corner,corner,z,0,1,0).
adjacency(strict,corner,wall,z,0,1,0).
adjacency(strict,corner,window,z,0,1,0).
adjacency(strict,corner,flatsurface,minusz,0,0,0).
adjacency(strict,corner,flatsurface,minusz,0,1,0).
adjacency(strict,corner,flatsurface,minusz,0,3,0).
adjacency(strict,corner,flatsurface,minusz,0,2,0).
adjacency(strict,corner,corner,minusz,0,1,0).
adjacency(strict,corner,corner,minusz,0,2,0).
adjacency(strict,corner,void,minusz,0,2,0).
adjacency(strict,corner,void,minusz,0,1,0).
adjacency(strict,corner,void,minusz,0,3,0).
adjacency(strict,corner,void,minusz,0,0,0).
adjacency(strict,corner,stairs,minusz,0,1,0).
adjacency(strict,corner,void_above_stairs,minusz,0,2,0).
adjacency(strict,corner,stairs,minusz,0,0,0).
adjacency(strict,corner,void_above_stairs,minusz,0,1,0).
adjacency(strict,corner,corner,minusy,0,1,0).
adjacency(strict,corner,corner,minusy,0,0,0).
adjacency(strict,corner,corner,minusy,0,2,0).
adjacency(strict,corner,window,minusy,0,2,0).
adjacency(strict,corner,corner,minusy,0,3,0).
adjacency(strict,corner,wall,minusy,0,1,0).
adjacency(strict,corner,flatsurface,minusy,0,0,0).
adjacency(strict,corner,flatsurface,minusy,0,1,0).
adjacency(strict,corner,void,minusy,0,1,0).
adjacency(strict,corner,flatsurface,minusy,0,3,0).
adjacency(strict,corner,flatsurface,minusy,0,2,0).
adjacency(strict,corner,door,minusy,0,2,0).
adjacency(strict,corner,door,minusy,0,3,0).
adjacency(strict,corner,wall,minusy,0,2,0).
adjacency(strict,corner,void_above_stairs,minusy,0,0,0).
adjacency(strict,corner,void_above_stairs,minusy,0,2,0).
adjacency(strict,corner,void_above_stairs,minusy,0,3,0).
adjacency(strict,corner,wall,minusy,0,0,0).
adjacency(strict,corner,window,minusy,0,1,0).
adjacency(strict,corner,void,minusy,0,0,0).
adjacency(strict,corner,window,minusy,0,0,0).
adjacency(strict,corner,void,minusy,0,3,0).
adjacency(strict,corner,void,minusy,0,2,0).
adjacency(strict,door,wall,z,0,2,0).
adjacency(strict,door,inside,z,0,3,0).
adjacency(strict,door,window,z,0,2,0).
adjacency(strict,door,inside,z,0,1,0).
adjacency(strict,door,inside,z,0,0,0).
adjacency(strict,door,inside,z,0,2,0).
adjacency(strict,door,door,z,0,2,0).
adjacency(strict,door,flatsurface,minusz,0,3,0).
adjacency(strict,door,flatsurface,minusz,0,2,0).
adjacency(strict,door,flatsurface,minusz,0,0,0).
adjacency(strict,door,flatsurface,minusz,0,1,0).
adjacency(strict,door,roof,y,0,3,0).
adjacency(strict,door,roof,y,0,0,0).
adjacency(strict,door,roof,y,0,1,0).
adjacency(strict,door,roof,y,0,2,0).
adjacency(strict,door,flatsurface,y,0,2,0).
adjacency(strict,door,inside,y,0,3,0).
adjacency(strict,door,door,y,0,2,0).
adjacency(strict,door,corner,y,0,2,0).
adjacency(strict,door,flatsurface,y,0,0,0).
adjacency(strict,door,corner,y,0,1,0).
adjacency(strict,door,flatsurface,y,0,1,0).
adjacency(strict,door,inside,y,0,0,0).
adjacency(strict,door,flatsurface,y,0,3,0).
adjacency(strict,door,window,y,0,0,0).
adjacency(strict,door,door,y,0,0,0).
adjacency(strict,door,door,y,0,3,0).
adjacency(strict,door,door,y,0,1,0).
adjacency(strict,door,wall,y,0,1,0).
adjacency(strict,door,corner,minusx,0,0,0).
adjacency(strict,door,wall,minusx,0,0,0).
adjacency(strict,door,corner,x,0,3,0).
adjacency(strict,door,wall,x,0,0,0).
adjacency(strict,door,flatsurface,minusy,0,2,0).
adjacency(strict,door,corner,minusy,0,2,0).
adjacency(strict,door,flatsurface,minusy,0,3,0).
adjacency(strict,door,door,minusy,0,2,0).
adjacency(strict,door,corner,minusy,0,1,0).
adjacency(strict,door,corner,minusy,0,3,0).
adjacency(strict,door,flatsurface,minusy,0,0,0).
adjacency(strict,door,corner,minusy,0,0,0).
adjacency(strict,door,flatsurface,minusy,0,1,0).
adjacency(strict,door,void,minusy,0,0,0).
adjacency(strict,door,door,minusy,0,0,0).
adjacency(strict,door,door,minusy,0,1,0).
adjacency(strict,door,door,minusy,0,3,0).
adjacency(strict,door,void,minusy,0,3,0).
adjacency(strict,door,inside,minusy,0,2,0).
adjacency(strict,door,void_above_stairs,minusy,0,3,0).
adjacency(strict,wall,flatsurface,minusz,0,1,0).
adjacency(strict,wall,flatsurface,minusz,0,0,0).
adjacency(strict,wall,flatsurface,minusz,0,2,0).
adjacency(strict,wall,flatsurface,minusz,0,3,0).
adjacency(strict,wall,stairs,minusz,0,1,0).
adjacency(strict,wall,void,minusz,0,3,0).
adjacency(strict,wall,void,minusz,0,2,0).
adjacency(strict,wall,void_above_stairs,minusz,0,3,0).
adjacency(strict,wall,stairs,minusz,0,3,0).
adjacency(strict,wall,stairs,minusz,0,0,0).
adjacency(strict,wall,void,minusz,0,0,0).
adjacency(strict,wall,void_above_stairs,minusz,0,1,0).
adjacency(strict,wall,void,minusz,0,1,0).
adjacency(strict,wall,door,z,0,2,0).
adjacency(strict,wall,inside,z,0,0,0).
adjacency(strict,wall,inside,z,0,1,0).
adjacency(strict,wall,inside,z,0,2,0).
adjacency(strict,wall,inside,z,0,3,0).
adjacency(strict,wall,window,z,0,2,0).
adjacency(strict,wall,wall,z,0,2,0).
adjacency(strict,wall,roof,y,0,1,0).
adjacency(strict,wall,roof,y,0,0,0).
adjacency(strict,wall,roof,y,0,2,0).
adjacency(strict,wall,flatsurface,y,0,0,0).
adjacency(strict,wall,corner,y,0,3,0).
adjacency(strict,wall,flatsurface,y,0,2,0).
adjacency(strict,wall,stairs,y,0,3,0).
adjacency(strict,wall,corner,y,0,2,0).
adjacency(strict,wall,window,y,0,0,0).
adjacency(strict,wall,flatsurface,y,0,3,0).
adjacency(strict,wall,flatsurface,y,0,1,0).
adjacency(strict,wall,wall,y,0,0,0).
adjacency(strict,wall,corner,y,0,0,0).
adjacency(strict,wall,roof,y,0,3,0).
adjacency(strict,wall,corner,x,0,3,0).
adjacency(strict,wall,door,x,0,0,0).
adjacency(strict,wall,wall,x,0,0,0).
adjacency(strict,wall,corner,minusx,0,0,0).
adjacency(strict,wall,door,minusx,0,0,0).
adjacency(strict,wall,wall,minusx,0,0,0).
adjacency(strict,wall,window,minusx,0,0,0).
adjacency(strict,wall,flatsurface,minusy,0,2,0).
adjacency(strict,wall,corner,minusy,0,3,0).
adjacency(strict,wall,corner,minusy,0,0,0).
adjacency(strict,wall,void,minusy,0,2,0).
adjacency(strict,wall,flatsurface,minusy,0,3,0).
adjacency(strict,wall,wall,minusy,0,0,0).
adjacency(strict,wall,flatsurface,minusy,0,0,0).
adjacency(strict,wall,void,minusy,0,1,0).
adjacency(strict,wall,door,minusy,0,3,0).
adjacency(strict,wall,flatsurface,minusy,0,1,0).
adjacency(strict,wall,void,minusy,0,3,0).
adjacency(strict,wall,window,minusy,0,0,0).
adjacency(strict,inside,wall,x,0,3,0).
adjacency(strict,inside,door,x,0,3,0).
adjacency(strict,inside,window,x,0,3,0).
adjacency(strict,inside,inside,x,0,0,0).
adjacency(strict,inside,door,minusx,0,1,0).
adjacency(strict,inside,wall,minusx,0,1,0).
adjacency(strict,inside,window,minusx,0,1,0).
adjacency(strict,inside,inside,minusx,0,0,0).
adjacency(strict,inside,roof,y,0,0,0).
adjacency(strict,inside,flatsurface,y,0,0,0).
adjacency(strict,inside,door,y,0,2,0).
adjacency(strict,inside,inside,y,0,0,0).
adjacency(strict,inside,wall,z,0,2,0).
adjacency(strict,inside,window,z,0,2,0).
adjacency(strict,inside,inside,z,0,0,0).
adjacency(strict,inside,door,z,0,2,0).
adjacency(strict,inside,wall,minusz,0,0,0).
adjacency(strict,inside,window,minusz,0,0,0).
adjacency(strict,inside,inside,minusz,0,0,0).
adjacency(strict,inside,door,minusz,0,0,0).
adjacency(strict,inside,door,minusy,0,1,0).
adjacency(strict,inside,door,minusy,0,0,0).
adjacency(strict,inside,inside,minusy,0,0,0).
adjacency(strict,window,door,z,0,2,0).
adjacency(strict,window,inside,z,0,0,0).
adjacency(strict,window,inside,z,0,2,0).
adjacency(strict,window,inside,z,0,1,0).
adjacency(strict,window,inside,z,0,3,0).
adjacency(strict,window,wall,z,0,2,0).
adjacency(strict,window,roof,y,0,1,0).
adjacency(strict,window,roof,y,0,3,0).
adjacency(strict,window,roof,y,0,2,0).
adjacency(strict,window,roof,y,0,0,0).
adjacency(strict,window,corner,y,0,2,0).
adjacency(strict,window,flatsurface,y,0,3,0).
adjacency(strict,window,window,y,0,0,0).
adjacency(strict,window,stairs,y,0,3,0).
adjacency(strict,window,flatsurface,y,0,0,0).
adjacency(strict,window,flatsurface,y,0,2,0).
adjacency(strict,window,corner,y,0,3,0).
adjacency(strict,window,flatsurface,y,0,1,0).
adjacency(strict,window,corner,y,0,0,0).
adjacency(strict,window,wall,y,0,0,0).
adjacency(strict,window,corner,x,0,3,0).
adjacency(strict,window,window,x,0,0,0).
adjacency(strict,window,wall,x,0,0,0).
adjacency(strict,window,corner,minusx,0,0,0).
adjacency(strict,window,window,minusx,0,0,0).
adjacency(strict,window,flatsurface,minusz,0,0,0).
adjacency(strict,window,flatsurface,minusz,0,3,0).
adjacency(strict,window,flatsurface,minusz,0,2,0).
adjacency(strict,window,flatsurface,minusz,0,1,0).
adjacency(strict,window,void,minusz,0,2,0).
adjacency(strict,window,void,minusz,0,3,0).
adjacency(strict,window,void,minusz,0,1,0).
adjacency(strict,window,void,minusz,0,0,0).
adjacency(strict,window,void_above_stairs,minusz,0,3,0).
adjacency(strict,window,flatsurface,minusy,0,0,0).
adjacency(strict,window,flatsurface,minusy,0,3,0).
adjacency(strict,window,void_above_stairs,minusy,0,1,0).
adjacency(strict,window,corner,minusy,0,3,0).
adjacency(strict,window,wall,minusy,0,0,0).
adjacency(strict,window,window,minusy,0,0,0).
adjacency(strict,window,door,minusy,0,0,0).
adjacency(strict,window,corner,minusy,0,0,0).
adjacency(strict,window,void,minusy,0,3,0).
adjacency(strict,window,void,minusy,0,1,0).
adjacency(strict,window,flatsurface,minusy,0,1,0).
adjacency(strict,stairs,wall,minusx,0,3,0).
adjacency(strict,stairs,corner,minusx,0,3,0).
adjacency(strict,stairs,flatsurface,minusx,0,3,0).
adjacency(strict,stairs,void_above_stairs,minusx,0,0,0).
adjacency(strict,stairs,flatsurface,minusx,0,0,0).
adjacency(strict,stairs,void_above_stairs,minusx,0,2,0).
adjacency(strict,stairs,void,minusx,0,0,0).
adjacency(strict,stairs,flatsurface,minusx,0,1,0).
adjacency(strict,stairs,flatsurface,minusx,0,2,0).
adjacency(strict,stairs,void,minusx,0,1,0).
adjacency(strict,stairs,corner,x,0,0,0).
adjacency(strict,stairs,wall,x,0,1,0).
adjacency(strict,stairs,flatsurface,x,0,3,0).
adjacency(strict,stairs,flatsurface,x,0,0,0).
adjacency(strict,stairs,flatsurface,x,0,1,0).
adjacency(strict,stairs,void,x,0,1,0).
adjacency(strict,stairs,flatsurface,x,0,2,0).
adjacency(strict,stairs,void,x,0,3,0).
adjacency(strict,stairs,void,x,0,0,0).
adjacency(strict,stairs,void,x,0,2,0).
adjacency(strict,stairs,flatsurface,minusz,0,2,0).
adjacency(strict,stairs,flatsurface,minusz,0,1,0).
adjacency(strict,stairs,flatsurface,minusz,0,3,0).
adjacency(strict,stairs,void_above_stairs,minusz,0,0,0).
adjacency(strict,stairs,flatsurface,minusz,0,0,0).
adjacency(strict,stairs,flatsurface,z,0,2,0).
adjacency(strict,stairs,flatsurface,z,0,1,0).
adjacency(strict,stairs,corner,z,0,3,0).
adjacency(strict,stairs,flatsurface,z,0,3,0).
adjacency(strict,stairs,corner,z,0,0,0).
adjacency(strict,stairs,wall,z,0,0,0).
adjacency(strict,stairs,void,z,0,0,0).
adjacency(strict,stairs,void,z,0,1,0).
adjacency(strict,stairs,void,z,0,3,0).
adjacency(strict,stairs,void,z,0,2,0).
adjacency(strict,stairs,flatsurface,z,0,0,0).
adjacency(strict,stairs,corner,minusy,0,3,0).
adjacency(strict,stairs,wall,minusy,0,1,0).
adjacency(strict,stairs,flatsurface,minusy,0,3,0).
adjacency(strict,stairs,flatsurface,minusy,0,0,0).
adjacency(strict,stairs,flatsurface,minusy,0,1,0).
adjacency(strict,stairs,window,minusy,0,1,0).
adjacency(strict,stairs,void,minusy,0,2,0).
adjacency(strict,stairs,void,minusy,0,3,0).
adjacency(strict,stairs,flatsurface,minusy,0,2,0).
adjacency(strict,stairs,corner,minusy,0,0,0).
adjacency(strict,stairs,void,minusy,0,1,0).
adjacency(strict,stairs,corner,minusy,0,1,0).
adjacency(strict,stairs,void,minusy,0,0,0).
adjacency(strict,stairs,void_above_stairs,y,0,0,0).
adjacency(strict,void_above_stairs,flatsurface,z,0,3,0).
adjacency(strict,void_above_stairs,stairs,z,0,0,0).
adjacency(strict,void_above_stairs,flatsurface,z,0,0,0).
adjacency(strict,void_above_stairs,flatsurface,z,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,z,0,2,0).
adjacency(strict,void_above_stairs,corner,minusz,0,2,0).
adjacency(strict,void_above_stairs,void,minusz,0,3,0).
adjacency(strict,void_above_stairs,void,minusz,0,0,0).
adjacency(strict,void_above_stairs,void,minusz,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,minusz,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,minusz,0,3,0).
adjacency(strict,void_above_stairs,corner,minusz,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,minusz,0,0,0).
adjacency(strict,void_above_stairs,void,minusz,0,2,0).
adjacency(strict,void_above_stairs,stairs,minusy,0,0,0).
adjacency(strict,void_above_stairs,void,minusx,0,3,0).
adjacency(strict,void_above_stairs,corner,minusx,0,3,0).
adjacency(strict,void_above_stairs,stairs,minusx,0,2,0).
adjacency(strict,void_above_stairs,corner,minusx,0,2,0).
adjacency(strict,void_above_stairs,void,minusx,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,minusx,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,minusx,0,0,0).
adjacency(strict,void_above_stairs,void,minusx,0,0,0).
adjacency(strict,void_above_stairs,void,minusx,0,2,0).
adjacency(strict,void_above_stairs,flatsurface,minusx,0,2,0).
adjacency(strict,void_above_stairs,wall,minusx,0,3,0).
adjacency(strict,void_above_stairs,flatsurface,minusx,0,3,0).
adjacency(strict,void_above_stairs,wall,x,0,1,0).
adjacency(strict,void_above_stairs,corner,x,0,0,0).
adjacency(strict,void_above_stairs,flatsurface,x,0,3,0).
adjacency(strict,void_above_stairs,stairs,x,0,0,0).
adjacency(strict,void_above_stairs,void,x,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,x,0,0,0).
adjacency(strict,void_above_stairs,void,x,0,0,0).
adjacency(strict,void_above_stairs,void,x,0,3,0).
adjacency(strict,void_above_stairs,void,x,0,2,0).
adjacency(strict,void_above_stairs,flatsurface,x,0,1,0).
adjacency(strict,void_above_stairs,window,x,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,y,0,3,0).
adjacency(strict,void_above_stairs,void,y,0,3,0).
adjacency(strict,void_above_stairs,window,y,0,3,0).
adjacency(strict,void_above_stairs,void,y,0,1,0).
adjacency(strict,void_above_stairs,flatsurface,y,0,0,0).
adjacency(strict,void_above_stairs,corner,y,0,0,0).
adjacency(strict,void_above_stairs,corner,y,0,2,0).
adjacency(strict,void_above_stairs,corner,y,0,1,0).
adjacency(strict,void_above_stairs,void,y,0,2,0).
adjacency(strict,void_above_stairs,void,y,0,0,0).
adjacency(strict,void_above_stairs,flatsurface,y,0,2,0).
adjacency(strict,void_above_stairs,door,y,0,1,0).


%adjacencies for Type: routing.
%adjacency(Type, ID1, ID2, D, Rx, Ry, Rz).
adjacency(routing,stairs,flatsurface,minusz,0,2,0).
adjacency(routing,stairs,flatsurface,minusz,0,1,0).
adjacency(routing,stairs,flatsurface,minusz,0,3,0).
adjacency(routing,stairs,void_above_stairs,minusz,0,0,0).
adjacency(routing,stairs,flatsurface,minusz,0,0,0).
adjacency(routing,stairs,void_above_stairs,y,0,0,0).
adjacency(routing,void_above_stairs,stairs,minusy,0,0,0).
adjacency(routing,void_above_stairs,flatsurface,z,0,3,0).
adjacency(routing,void_above_stairs,stairs,z,0,0,0).
adjacency(routing,void_above_stairs,flatsurface,z,0,0,0).
adjacency(routing,void_above_stairs,flatsurface,z,0,1,0).
adjacency(routing,void_above_stairs,flatsurface,z,0,2,0).
adjacency(routing,flatsurface,flatsurface,x,0,0,0).
adjacency(routing,flatsurface,door,x,0,1,0).
adjacency(routing,flatsurface,stairs,x,0,1,0).
adjacency(routing,flatsurface,void_above_stairs,x,0,3,0).
adjacency(routing,flatsurface,flatsurface,minusx,0,0,0).
adjacency(routing,flatsurface,door,minusx,0,3,0).
adjacency(routing,flatsurface,stairs,minusx,0,3,0).
adjacency(routing,flatsurface,void_above_stairs,minusx,0,1,0).
adjacency(routing,flatsurface,flatsurface,z,0,0,0).
adjacency(routing,flatsurface,door,z,0,0,0).
adjacency(routing,flatsurface,stairs,z,0,0,0).
adjacency(routing,flatsurface,void_above_stairs,z,0,2,0).
adjacency(routing,flatsurface,flatsurface,minusz,0,0,0).
adjacency(routing,flatsurface,door,minusz,0,2,0).
adjacency(routing,flatsurface,stairs,minusz,0,2,0).
adjacency(routing,flatsurface,void_above_stairs,minusz,0,0,0).
adjacency(routing,door,corner,x,0,3,0).
adjacency(routing,door,wall,x,0,0,0).
adjacency(routing,door,corner,minusx,0,0,0).
adjacency(routing,door,wall,minusx,0,0,0).
adjacency(routing,door,wall,z,0,2,0).
adjacency(routing,door,inside,z,0,3,0).
adjacency(routing,door,window,z,0,2,0).
adjacency(routing,door,inside,z,0,1,0).
adjacency(routing,door,inside,z,0,0,0).
adjacency(routing,door,inside,z,0,2,0).
adjacency(routing,door,door,z,0,2,0).
adjacency(routing,door,flatsurface,minusz,0,3,0).
adjacency(routing,door,flatsurface,minusz,0,2,0).
adjacency(routing,door,flatsurface,minusz,0,0,0).
adjacency(routing,door,flatsurface,minusz,0,1,0).
adjacency(routing,window,corner,minusx,0,0,0).
adjacency(routing,window,window,minusx,0,0,0).
adjacency(routing,window,corner,x,0,3,0).
adjacency(routing,window,window,x,0,0,0).
adjacency(routing,window,wall,x,0,0,0).
adjacency(routing,window,door,z,0,2,0).
adjacency(routing,window,inside,z,0,0,0).
adjacency(routing,window,inside,z,0,2,0).
adjacency(routing,window,inside,z,0,1,0).
adjacency(routing,window,inside,z,0,3,0).
adjacency(routing,window,wall,z,0,2,0).
adjacency(routing,wall,corner,minusx,0,0,0).
adjacency(routing,wall,door,minusx,0,0,0).
adjacency(routing,wall,wall,minusx,0,0,0).
adjacency(routing,wall,window,minusx,0,0,0).
adjacency(routing,wall,corner,x,0,3,0).
adjacency(routing,wall,door,x,0,0,0).
adjacency(routing,wall,wall,x,0,0,0).
adjacency(routing,wall,door,z,0,2,0).
adjacency(routing,wall,inside,z,0,0,0).
adjacency(routing,wall,inside,z,0,1,0).
adjacency(routing,wall,inside,z,0,2,0).
adjacency(routing,wall,inside,z,0,3,0).
adjacency(routing,wall,window,z,0,2,0).
adjacency(routing,wall,wall,z,0,2,0).
adjacency(routing,corner,door,z,0,1,0).
adjacency(routing,corner,corner,z,0,1,0).
adjacency(routing,corner,wall,z,0,1,0).
adjacency(routing,corner,window,z,0,1,0).
adjacency(routing,corner,corner,x,0,3,0).
adjacency(routing,corner,wall,x,0,0,0).
adjacency(routing,corner,door,x,0,0,0).
adjacency(routing,corner,window,x,0,0,0).
adjacency(routing,inside,wall,x,0,3,0).
adjacency(routing,inside,door,x,0,3,0).
adjacency(routing,inside,window,x,0,3,0).
adjacency(routing,inside,inside,x,0,0,0).
adjacency(routing,inside,door,minusx,0,1,0).
adjacency(routing,inside,wall,minusx,0,1,0).
adjacency(routing,inside,window,minusx,0,1,0).
adjacency(routing,inside,inside,minusx,0,0,0).
adjacency(routing,inside,wall,z,0,2,0).
adjacency(routing,inside,window,z,0,2,0).
adjacency(routing,inside,inside,z,0,0,0).
adjacency(routing,inside,door,z,0,2,0).
adjacency(routing,inside,wall,minusz,0,0,0).
adjacency(routing,inside,window,minusz,0,0,0).
adjacency(routing,inside,inside,minusz,0,0,0).
adjacency(routing,inside,door,minusz,0,0,0).

%adjacencies for Type: construction.
%adjacency(Type, ID1, ID2, D, Rx, Ry, Rz).
adjacency(construction,stairs,corner,minusy,0,3,0).
adjacency(construction,stairs,wall,minusy,0,1,0).
adjacency(construction,stairs,window,minusy,0,1,0).
adjacency(construction,stairs,corner,minusy,0,0,0).
adjacency(construction,stairs,corner,minusy,0,1,0).
adjacency(construction,stairs,void_above_stairs,y,0,0,0).
adjacency(construction,void_above_stairs,stairs,minusy,0,0,0).
adjacency(construction,door,corner,x,0,3,0).
adjacency(construction,door,wall,x,0,0,0).
adjacency(construction,door,corner,minusx,0,0,0).
adjacency(construction,door,wall,minusx,0,0,0).
adjacency(construction,door,wall,z,0,2,0).
adjacency(construction,door,inside,z,0,3,0).
adjacency(construction,door,window,z,0,2,0).
adjacency(construction,door,inside,z,0,1,0).
adjacency(construction,door,inside,z,0,0,0).
adjacency(construction,door,inside,z,0,2,0).
adjacency(construction,door,door,z,0,2,0).
adjacency(construction,door,roof,y,0,3,0).
adjacency(construction,door,roof,y,0,0,0).
adjacency(construction,door,roof,y,0,1,0).
adjacency(construction,door,roof,y,0,2,0).
adjacency(construction,window,corner,x,0,3,0).
adjacency(construction,window,window,x,0,0,0).
adjacency(construction,window,wall,x,0,0,0).
adjacency(construction,window,corner,minusx,0,0,0).
adjacency(construction,window,window,minusx,0,0,0).
adjacency(construction,window,door,z,0,2,0).
adjacency(construction,window,inside,z,0,0,0).
adjacency(construction,window,inside,z,0,2,0).
adjacency(construction,window,inside,z,0,1,0).
adjacency(construction,window,inside,z,0,3,0).
adjacency(construction,window,wall,z,0,2,0).
adjacency(construction,window,roof,y,0,1,0).
adjacency(construction,window,roof,y,0,3,0).
adjacency(construction,window,roof,y,0,2,0).
adjacency(construction,window,roof,y,0,0,0).
adjacency(construction,window,stairs,y,0,3,0).
adjacency(construction,wall,corner,x,0,3,0).
adjacency(construction,wall,door,x,0,0,0).
adjacency(construction,wall,wall,x,0,0,0).
adjacency(construction,wall,corner,minusx,0,0,0).
adjacency(construction,wall,door,minusx,0,0,0).
adjacency(construction,wall,wall,minusx,0,0,0).
adjacency(construction,wall,window,minusx,0,0,0).
adjacency(construction,wall,door,z,0,2,0).
adjacency(construction,wall,inside,z,0,0,0).
adjacency(construction,wall,inside,z,0,1,0).
adjacency(construction,wall,inside,z,0,2,0).
adjacency(construction,wall,inside,z,0,3,0).
adjacency(construction,wall,window,z,0,2,0).
adjacency(construction,wall,wall,z,0,2,0).
adjacency(construction,wall,roof,y,0,1,0).
adjacency(construction,wall,roof,y,0,0,0).
adjacency(construction,wall,roof,y,0,2,0).
adjacency(construction,wall,stairs,y,0,3,0).
adjacency(construction,wall,roof,y,0,3,0).
adjacency(construction,corner,corner,x,0,3,0).
adjacency(construction,corner,wall,x,0,0,0).
adjacency(construction,corner,door,x,0,0,0).
adjacency(construction,corner,window,x,0,0,0).
adjacency(construction,corner,door,z,0,1,0).
adjacency(construction,corner,corner,z,0,1,0).
adjacency(construction,corner,wall,z,0,1,0).
adjacency(construction,corner,window,z,0,1,0).
adjacency(construction,corner,roof,y,0,0,0).
adjacency(construction,corner,roof,y,0,1,0).
adjacency(construction,corner,roof,y,0,3,0).
adjacency(construction,corner,roof,y,0,2,0).
adjacency(construction,corner,stairs,y,0,1,0).
adjacency(construction,corner,stairs,y,0,0,0).
adjacency(construction,corner,stairs,y,0,3,0).
adjacency(construction,inside,roof,y,0,0,0).
adjacency(construction,inside,wall,x,0,3,0).
adjacency(construction,inside,door,x,0,3,0).
adjacency(construction,inside,window,x,0,3,0).
adjacency(construction,inside,inside,x,0,0,0).
adjacency(construction,inside,wall,z,0,2,0).
adjacency(construction,inside,window,z,0,2,0).
adjacency(construction,inside,inside,z,0,0,0).
adjacency(construction,inside,door,z,0,2,0).
adjacency(construction,inside,wall,minusz,0,0,0).
adjacency(construction,inside,window,minusz,0,0,0).
adjacency(construction,inside,inside,minusz,0,0,0).
adjacency(construction,inside,door,minusz,0,0,0).
adjacency(construction,inside,door,minusx,0,1,0).
adjacency(construction,inside,wall,minusx,0,1,0).
adjacency(construction,inside,window,minusx,0,1,0).
adjacency(construction,inside,inside,minusx,0,0,0).
adjacency(construction,roof,corner,minusy,0,0,0).
adjacency(construction,roof,corner,minusy,0,3,0).
adjacency(construction,roof,door,minusy,0,1,0).
adjacency(construction,roof,wall,minusy,0,3,0).
adjacency(construction,roof,corner,minusy,0,1,0).
adjacency(construction,roof,corner,minusy,0,2,0).
adjacency(construction,roof,wall,minusy,0,0,0).
adjacency(construction,roof,inside,minusy,0,0,0).
adjacency(construction,roof,wall,minusy,0,2,0).
adjacency(construction,roof,window,minusy,0,3,0).
adjacency(construction,roof,door,minusy,0,0,0).
adjacency(construction,roof,window,minusy,0,1,0).
adjacency(construction,roof,door,minusy,0,3,0).
adjacency(construction,roof,window,minusy,0,2,0).
adjacency(construction,roof,door,minusy,0,2,0).
adjacency(construction,roof,window,minusy,0,0,0).
adjacency(construction,roof,wall,minusy,0,1,0).

softoverride.




% set metaposition if this block is the final edge of the solution in a certain direction
metaposition(0,x).
metaposition(0,minusx).
metaposition(0,y).
metaposition(0,minusy).
metaposition(0,z).
metaposition(0,minusz).




% certain blobs are forced to be connected to an edge of the solution.
connectivitytype(directconstruction).
relevantthroughcategory(built).
blobtoside(directconstruction,built,minusy).
% connectivity blobs
connectivitytype(directconstruction).
relevantthroughcategory(interior).
connectivityrangenums(0..6).
requireddistance(directconstruction, interior, 0, 6, 0, 1, 0, 6).

% if blob A and blob C exist then there must be blob B connecting them


% Assignments of already solved adjacent blocks that this block needs to unify with.

% Density weights for categories.
densityweight(void, -1).
densityweight(interior, 1).




tilesolvingmode.

% simple connected
simpleallconnected(routing, routing).
connectivitytype(routing).


#show shapeplacement/1.
#show validshapeposition/4.
#show placedshapeposition/4.
#show shapeallocationspace/3.

% TURN ON densityoptimization
%densityoptimization.

% amount of textures with a certain tag.
textureswithtag(T, A) :- densityoptimization, A = #count{X,Y,Z: assign(X,Y,Z,ID, _, _, _), tile(ID), not override(X,Y,Z,T),
currentblock(_, X,Y,Z), category(ID, T)}, category(_, T).

% maximize density weights
% implementation from Adam Smith
%assigned_id((X,Y,Z),I) :- assigned(X,Y,Z,I,RX,RY,RZ).
%#maximize{ Weight@3,Cell: assigned_id(Cell,I), category(I,T), densityweight(T,Weight) }.

texturescore(S) :- densityoptimization,
S = #sum{ I : textureswithtag(T,A), densityweight(T, W), I = A * W}.
% #maximize{ A@3,Cell: cell(Cell), texturescore(A) }.

#show texturescore/1.
#show textureswithtag/2.

% TURN ON uniquetilesoptimization
% uniquetilesoptimization.
% Sum the unique groups that can be identified in the assigned cells.
uniquetiles(S) :- S = #count{ID : tile(ID), assign(_,_,_, ID, _, _, _)}.
% optimization to create as much variety as possible, by maximizing the amount of texturegroups present.
#maximize { Y@2, uniquetilesoptimization, X: tile(X), assign(_,_,_,X, _, _, _), uniquetiles(Y) }.
