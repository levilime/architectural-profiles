# Architectural Profiles for Procedural content generation

Code used to generate the results for [Declarative procedural generation of architecture with semantic architectural profiles](https://graphics.tudelft.nl/Publications-new/2020/AB20/) paper.

The project uses `Poetry` for managing the python dependencies.

To generate the experimental results: `python run_experiments.py` , the results will be aggregated in the experiments folder.
To output the [Expressive range](https://www.researchgate.net/publication/228411962_Analyzing_the_expressive_range_of_a_level_generator) after running the experiments: `python expressiverange.py`

(Code does not come with any guaranties and warranties :smile: )

##  Context


Part of a thesis project to investigate the applicability of tile solving to create large architectural spaces.
Here the user inputs a set of n-dimensional tiles. The edges of the tiles decide the constraints
between the tiles as they should connect. Then for a grid in which these tiles must be placed,
a selection of tiles should be placed that fit the constraints of the tileset.

This constraint problem is proven to be NP-Hard. Multiple suggestions have been done in the literature
to solve this constraint problem heuristically. Such as Discrete model synthesis and
Wave function collapse. This Tile-solver supports adding semantics to tiles, to improve the controllability of
the solution.

This project gives an n-dimensional implementation of solving the tileset. For 2Dimensional space images
can be given as input and are given as output. For higher dimensional space the input tiles are coded as
boolean arrays. If they are 3Dimensional space than the output can be given in the .vox format associated
with MagicaVoxel. Because MagicaVoxel only supports a limited view size (128 voxels in one dimension) the
results (`.vox`) are visualized with [Goxel](http://guillaumechereau.github.io/goxel/) or [MagicaVoxel](https://ephtracy.github.io/)

## Important academic references

- [Model Synthesis](http://graphics.stanford.edu/~pmerrell/thesis.pdf) by Paul Merrel.
- [Wave Function Collapse](https://github.com/mxgmn/WaveFunctionCollapse) by mxgmm.
- [Tile constraint solving with Clingo](https://adamsmith.as/papers/wfc_is_constraint_solving_in_the_wild.pdf) by Isaac Karth and Adam M. Smith.

## Installation

Python libraries used:
- numpy
- py-vox-io (for generating .vox files for magicavoxel or goxel)
- Pillow

This is very much a research in progress and things will change often. The current external programs
are used that call or are called by this project.

- [Clingo](https://potassco.org/clingo/)
- [Goxel](http://guillaumechereau.github.io/goxel/)
- [MagicaVoxel](https://ephtracy.github.io/)


### Clingo

Clingo can be used in this project by adding it as a environment variable. It is used to solve tiles.
It can be [downloaded here](https://github.com/potassco/clingo/releases).

### Goxel

Goxel is an adequate voxel visualizer. To use it with the code, the directory needs to be put in this project. Specifically
the directory called `goxel.exe` that can be [downloaded here](http://guillaumechereau.github.io/goxel/downloads) needs to be put in the project directory.

### Magica Voxel

MagicaVoxel is a nice looking voxel visualizer but closed source and with limited applicability due to an edit space limit of
126 in each dimension. It has been used in the project before Goxel and may be used in some old parts of the code
to visualize things.

### Ipyvolume

Ipyvolume is used to visualize results interactively in jupyter notebooks. To use the gif creation functionality Imagemick needs to be installed.

## Profile Specification

Profiles are written as a json. The `profiles` folder contains examples.