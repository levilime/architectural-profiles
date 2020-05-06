
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
