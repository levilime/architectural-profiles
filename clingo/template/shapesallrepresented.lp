
hasshapegeneral(Name) :- shapecontainer(Name, SID), 1 {placedshapeposition((SID, _, _), _, _, _)}.
%:- not 1 {hasshapegeneral(_)}, shapesolvingmode.
% all shape represented is ignored if there is a shapeoccurence requirement
:- shapecontainer(Name, _), not hasshapegeneral(Name), shapesolvingmode,
  not shapeoccurence(_,_,_).
