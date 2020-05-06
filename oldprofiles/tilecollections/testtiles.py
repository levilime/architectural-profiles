from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.tiles import empty_space


class TestTileSet(AbstractBuilder):

    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        normal_tiles = [
            VolumeTexture("empty_space_outside",
                          empty_space(match_shape),
                          empty_space(visual_shape),
                          ["empty", "outside", "void"]),
            *super().VTOM("inner",
                          inner(visual_shape),
                          ["test"]),
            *super().VTOM("forward",
                          forward(visual_shape),
                          ["test"]),
            *super().VTOM("backward",
                          backward(visual_shape),
                          ["test"]),
            *super().VTOM("left",
                          left(visual_shape),
                          ["test"]),
            *super().VTOM("right",
                          right(visual_shape),
                          ["test"]),
            *super().VTOM("up",
                          up(visual_shape),
                          ["test"]),
            *super().VTOM("down",
                          down(visual_shape),
                          ["test"]),
        ]
        self.realized_textures = super().create_tiles([], [], normal_tiles)

def inner(shape):
    M = empty_space(shape)
    M[0, 3, 3] = True
    M[0, 3, 4] = True
    M[-1, 3, 3] = True
    M[-1, 3, 2] = True
    M[3, 3, 0] = True
    M[4, 3, 0] = True
    M[3, 3, -1] = True
    M[2, 3, -1] = True
    M[3, 0, 3] = True
    M[4, 0, 3] = True
    M[3, -1, 3] = True
    M[2, -1, 3] = True
    return M


def forward(shape):
    M = empty_space(shape)
    M[0, 3, 3] = True
    M[0, 3, 2] = True
    return M

def backward(shape):
    M = empty_space(shape)
    M[-1, 3, 3] = True
    M[-1, 3, 4] = True
    return M

def right(shape):
    M = empty_space(shape)
    M[3, 3, 0] = True
    M[2, 3, 0] = True
    return M

def left(shape):
    M = empty_space(shape)
    M[3, 3, -1] = True
    M[4, 3, -1] = True
    return M

def up(shape):
    M = empty_space(shape)
    M[3, 0, 3] = True
    M[2, 0, 3] = True
    return M

def down(shape):
    M = empty_space(shape)
    M[3, -1, 3] = True
    M[4, -1, 3] = True
    return M