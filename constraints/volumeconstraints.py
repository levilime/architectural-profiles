from constraints.volumetexture import VolumeTexture
from functools import reduce


class VolumeConstraints:

    def __init__(self, corpus):
        # self.realized_textures = corpus
        list(map(lambda texture: texture.resolve_overriding_edges(corpus), corpus))
        list(map(lambda texture: texture.add_constraints_from_corpus(corpus), corpus))
        self.realized_textures = corpus
        #
        # for texture in corpus:
        #     if texture.id.startswith("small_nook_side_door"):
        #         # texture.show_constraints()
        #         pass
        # self.realized_textures = reduce(lambda agg, texture: dict(agg, **{texture.id: texture}), textures, {})

