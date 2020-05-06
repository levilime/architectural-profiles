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
