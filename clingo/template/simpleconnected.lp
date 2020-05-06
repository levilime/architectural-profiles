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
