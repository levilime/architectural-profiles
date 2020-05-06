% whether a shape is closed within the input,
% used in finding non atomic shapes.
:- closedontype(Type), not tileswithininput(Type).

hasshape(Name) :- requiredshapeid(Name), 1 {shapeplacement((SID, _, _)): shapecontainer(Name, SID)}.
:- requiredshapeid(Name), not hasshape(Name).
