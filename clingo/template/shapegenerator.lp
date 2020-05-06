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
