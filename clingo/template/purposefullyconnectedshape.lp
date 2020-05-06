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
