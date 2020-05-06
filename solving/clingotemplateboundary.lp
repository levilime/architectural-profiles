% define?
cell(0..xsize, 0..ysize, 0..zsize).
currentblock(0..xsize, 0..ysize, 0..zsize).

% X, -X, Y, -Y, Z, -Z
% INSERT TEXTURE CONSTRAINTS HERE

% adjacent means that two cells are next to each other
adjacent(X1, Y1, Z1, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), |X1 - X2| == 1, |Y1 - Y2| == 0, |Z1 - Z2| == 0.
adjacent(X1, Y1, Z1, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), |X1 - X2| == 0, |Y1 - Y2| == 1, |Z1 - Z2| == 0.
adjacent(X1, Y1, Z1, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), |X1 - X2| == 0, |Y1 - Y2| == 0, |Z1 - Z2| == 1.

% commented boundary logic
% adjacency to neighboring boundary edge
% adjacenttoneighboredge(X,Y,Z):- cell(X,Y,Z), assign(X,Y,Z,_), boundarymatchobjective(_, X,Y,Z,_).

% so if dimension is positive ID1 is above, right or behind ID2
match(X1, Y1,Z1, X2, Y2, Z2, ID1, ID2) :-  texture(ID1, _, _, _, _, _, _), texture(ID2, _, _, _, _, _, _),
    adjacent(X1, Y1, Z1, X2, Y2, Z2), match(X1 - X2, Y1 - Y2, Z1 - Z2, ID1, ID2).

% match if texture A at one side fits with texture B on the opposite side of B.
match(1, 0, 0, ID1, ID2):- texture(ID1, _, A, _, _, _, _), texture(ID2, A, _, _, _ , _, _).
match(-1, 0, 0, ID1, ID2):- texture(ID1, A, _, _, _, _, _), texture(ID2, _, A, _, _ , _, _).
match(0, 1, 0, ID1, ID2):- texture(ID1, _, _, _, A, _, _), texture(ID2, _, _, A, _ , _, _).
match(0, -1, 0, ID1, ID2):- texture(ID1, _, _, A, _, _, _), texture(ID2, _, _, _, A, _, _).
match(0, 0, 1, ID1, ID2):- texture(ID1, _, _, _, _, _, A), texture(ID2, _, _, _, _ , A, _).
match(0, 0, -1, ID1, ID2):- texture(ID1, _, _, _, _, A, _), texture(ID2, _, _, _, _, _, A).

match(x, ID1, ID2):- match(1, 0, 0, ID1, ID2).
match(minusx, ID1, ID2):- match(-1, 0, 0, ID1, ID2).
match(y, ID1, ID2):- match(0, 1, 0, ID1, ID2).
match(minusy, ID1, ID2):- match(0, -1, 0, ID1, ID2).
match(z, ID1, ID2):- match(0, 0, 1, ID1, ID2).
match(minusz, ID1, ID2):- match(0, 0, -1, ID1, ID2).

direction(x).
direction(y).
direction(z).
direction(minusx).
direction(minusy).
direction(minusz).

oppositedirection(x, minusx).
oppositedirection(minusx, x).
oppositedirection(y, minusy).
oppositedirection(minusy, y).
oppositedirection(z, minusz).
oppositedirection(minusz, z).

edgepositions(x, X,Y,Z) :- cell(X,Y,Z), X = xsize.
edgepositions(minusx, X,Y,Z) :- cell(X,Y,Z), X = 0.
edgepositions(y, X,Y,Z) :- cell(X,Y,Z), Y = ysize.
edgepositions(minusy, X,Y,Z) :- cell(X,Y,Z), Y = 0.
edgepositions(z, X,Y,Z) :- cell(X,Y,Z), Z = zsize.
edgepositions(minusz, X,Y,Z) :- cell(X,Y,Z), Z = 0.

hasadjacacencytodirection(X1, Y1, Z1, 0) :- cell(X1, Y1, Z1), Z1 < zsize.
hasadjacacencytodirection(X1, Y1, Z1, 1) :- cell(X1, Y1, Z1), X1 < xsize.
hasadjacacencytodirection(X1, Y1, Z1, 2) :- cell(X1, Y1, Z1), Z1 > 0.
hasadjacacencytodirection(X1, Y1, Z1, 3) :- cell(X1, Y1, Z1), X1 > 0.

directiontoadjacency(X1, Y1, Z1, 0, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), X2 == X1, Y2 == Y1, Z2 == Z1 + 1.
directiontoadjacency(X1, Y1, Z1, 1, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), X2 == X1 + 1, Y2 == Y1, Z2 == Z1.
directiontoadjacency(X1, Y1, Z1, 2, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), X2 == X1, Y2 == Y1, Z2 == Z1 - 1.
directiontoadjacency(X1, Y1, Z1, 3, X2, Y2, Z2) :- cell(X1, Y1, Z1), cell(X2, Y2, Z2), X2 == X1 - 1, Y2 == Y1, Z2 == Z1.

directionmap(x, X1, Y1, Z1, X2, Y2, Z2) :- adjacent(X1, Y1, Z1, X2, Y2, Z2),  X2 = X1 + 1, Y2 = Y1, Z2 = Z1.
directionmap(minusx, X1, Y1, Z1, X2, Y2, Z2) :- adjacent(X1, Y1, Z1, X2, Y2, Z2), X2 = X1 - 1, Y2 = Y1, Z2 = Z1.
directionmap(z, X1, Y1, Z1, X2, Y2, Z2) :- adjacent(X1, Y1, Z1, X2, Y2, Z2), X2 = X1, Y2 = Y1, Z2 = Z1 + 1.
directionmap(minusz, X1, Y1, Z1, X2, Y2, Z2) :- adjacent(X1, Y1, Z1, X2, Y2, Z2), X2 = X1, Y2 = Y1, Z2 = Z1 - 1.
directionmap(y, X1, Y1, Z1, X2, Y2, Z2) :- adjacent(X1, Y1, Z1, X2, Y2, Z2), X2 = X1, Y2 = Y1 + 1, Z2 = Z1.
directionmap(minusy, X1, Y1, Z1, X2, Y2, Z2) :- adjacent(X1, Y1, Z1, X2, Y2, Z2), X2 = X1, Y2 = Y1 - 1, Z2 = Z1.

adjacentIDS(ID1, ID2) :- assign(X1, Y1, Z1, ID1), assign(X2, Y2, Z2, ID2), adjacent(X1, Y1, Z1, X2, Y2, Z2).

% every cell needs to have an assignment
1 {assign(X,Y,Z,ID): texture(ID, _ ,_ ,_ ,_,_ ,_)} 1 :- cell(X,Y,Z), currentblock(X,Y,Z).

% every assignment must adhere to hard constraints of its neighbors
% with currentblock:
% one of the tiles being matched needs to be in this block, the other may be in this block or another block
:- adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X1, Y1, Z1, ID1), currentblock(X1, Y1, Z1), assign(X2, Y2, Z2, ID2),
not 1 {assign(X2, Y2, Z2, ID2): match(X1, Y1, Z1, X2, Y2, Z2, ID1, ID2)}.

% Sum the unique groups that can be identified in the assigned cells.
uniquegroups(S) :- S = #count{I : texturegroup(Id, I), assign(_,_,_, Id)}.

% amount of textures with a certain tag.
textureswithtag(T, A) :- A = #count{I: assign(_,_,_,I), texture(I, _, _, _, _, _, _)}, category(_, T).

% INSERT CONSTRAINT BOUNDARY MATCH HERE

#show assign/4.