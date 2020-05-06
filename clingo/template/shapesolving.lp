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
