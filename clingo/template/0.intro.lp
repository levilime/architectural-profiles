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
